import nbformat as nbf
from nbconvert import PDFExporter
import os
import glob
from IPython.core.display import display, HTML
import hashlib
from . import headings
from .utils import *
from tqdm import tqdm

def generate_filtered(input_file):
    print("Processing %s"%input_file)
    student_notebook = load_notebook(input_file)
    filtered = filter_nb(student_notebook)
    return filtered

def generateSubmission(fileName,**kwargs):
    if not run_from_ipython():
        print("You can't run this command from outside the Jupyter Notebook!")
        return
    diffed = generate_filtered(fileName)
    header = headings.generate_header()
    if header is not None:
        diffed.cells.insert(0, header)
    print("Generated notebook and autograded")


    if export_notebook(diffed, fileName.replace('.ipynb','_submission'), **kwargs) is not None:
        display(HTML(
            """<h1><a href="%s" download> Download this and submit to gradescope!</a></h1>"""%(fileName.replace('.ipynb','_submission.pdf'))
            ))
    else:
        display(HTML(
            """<h2>LaTeX failed to parse. Please see error message above</h2>
            Try running one of these functions to debug:
            <ul>
            <li> gsExport.generateSubmission(debug=True) # See the full error message
            <li> gsExport.cell_by_cell() # See which cell is causing you grief
                </ul>
            Once you make a change, remember to save your notebook (Save and Checkpoint)
            """
            ))


def cell_by_cell(fileName):
    assert run_from_ipython(), "You can't run this command from outside the Jupyter Notebook!"

    diffed = generate_filtered(fileName)
    temp_nb = diffed.copy()

    for cell in tqdm(diffed.cells):
        if cell['cell_type'] == 'code':
            continue
        temp_nb.cells = [cell]
        error = has_error(temp_nb)

        if error is not None:
            print("""

            There is an error with the following cell:
            ==========================================================================

            %s

            ==========================================================================
            Here's the error message we were able to extract

            %s

            ==========================================================================
            """%(cell['source'],str(error)))

def fix_dollar_sign(cell):
    if 'cell_type' in cell and cell['cell_type'] == 'markdown':
        cell['source'] = cell['source'].replace('$ ','$').replace(' $','$')

def paraphrase(text,fromBegin=3,fromEnd=3):
    numLines = text.count('\n')
    if numLines < fromBegin + fromEnd:
        return text
    textSplit = text.split('\n')
    newParts = textSplit[:fromBegin]+ ['... Omitting %d lines ... '%(numLines-fromBegin-fromEnd)] + textSplit[-1*fromEnd:]
    return '\n'.join(newParts)


def clean_cells(cells):
    """
    Works in place
    """
    for cell in cells:
        execution_num = cell.get('execution_num')
        if 'outputs' in cell:
            # Too many images?
            if len([i for i in cell['outputs'] if 'data' in i and 'image/png' in i['data']]) > 3:
                print("It looks like you have a cell with 4 or more images")
                print("This may cause errors with the Gradescope submission!")

            # Paraphrase output
            for output in cell['outputs']:
                if output.get('output_type', 'NA') == 'stream' and 'text' in output:
                    output['text'] = paraphrase(output['text'])
                if output.get('output_type','NA') == 'execute_result':
                    if 'data' in output and 'text/plain' in output['data']:
                        output['data']['text/plain'] = paraphrase(output['data']['text/plain'])
                if output.get('output_type', 'NA') == 'error' and 'traceback' in output:
                    output['traceback'] = output['traceback'][:1]

        if 'source' in cell and (cell['source'].count('\n') > 30 or len(cell['source']) > 4000):
            print('Found a cell that has a little too much written in it; try to bring it down')
            print("Here's a preview of that cell: \n\n\n %s"%(cell['source'][:200]))

        fix_dollar_sign(cell)

def filter_nb(nb):
    """
        Returns a modified version of nb_new which contains no cells which are
        *similar* to any cells in nb_base. Further culls output to allow for good PDF generation

    """
    remove_all_whitespace = lambda string: "".join(string.split())
    getHash = lambda cell: hashlib.md5(remove_all_whitespace(cell['source']).encode('utf8')).hexdigest()

    newCells = []

    if 'checksums' not in nb['metadata']:
        nb['metadata']['checksums'] = list()

    numPageBreaks = len([cell for cell in nb['cells'] if '#newpage' in cell['source']])
    expectedNumPageBreaks = nb['metadata'].get('number_of_pagebreaks',numPageBreaks)
    assert numPageBreaks >= expectedNumPageBreaks,\
        ("The number of pagebreaks (%d) is fewer than the expected number of pagebreaks "
         "(%d). Did you accidentally delete any?") % (numPageBreaks, expectedNumPageBreaks)

    for cell in nb['cells']:
        if cell['metadata'].get('#student',False) or '#newpage' in cell['source']:
            newCells.append(cell)
        elif getHash(cell) not in nb['metadata']['checksums']:
            newCells.append(cell)

    clean_cells(newCells)

    parse_nb = nb.copy()
    parse_nb['cells'] = newCells
    return parse_nb
