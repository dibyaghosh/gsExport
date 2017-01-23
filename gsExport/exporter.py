import nbformat as nbf
from nbconvert import PDFExporter
import os
import glob
from IPython.core.display import display, HTML
from . import ok_grading
from . import headings
from .utils import *

def select_one(list_of_choices,message="Which of these files is your notebook?",errormessage="Couldn't find anything"):
	if len(list_of_choices) == 0:
		print(errormessage)
		raise RuntimeError(errormessage)
	if len(list_of_choices) == 1:
		return list_of_choices[0]
	print(message)
	for n,elem in enumerate(list_of_choices):
		print(n+1,elem)
	while True:
		try:
			n = int(input("Which item do you want? (1-%d)"%(len(list_of_choices))))
			return list_of_choices[n-1]
		except:
			print("Please put a valid choice")

def generateSubmission(toIpynb=False,**kwargs):
	if not run_from_ipython():
		print("You can't run this command from outside the Jupyter Notebook!")
		return


	input_file = select_one(glob.glob("./*.ipynb"), "Which of these files is your notebook?",\
			"Can't find your notebook")
	print("Processing %s"%input_file)
	student_notebook = load_notebook(input_file)


	input_file = select_one(glob.glob("./grading/*.ipynb"),"Which of these files is the base notebook?",\
		"Can't find your (reference) notebook; Please contact your instructor")
	print("Base Notebook processing %s"%input_file)
	instructor_notebook = load_notebook(input_file)


	diffed = compareThese(instructor_notebook,student_notebook)
	results = ok_grading.autograde_ipython()
	if results is not None:
		diffed.cells.insert(0,results)
	header = headings.generate_header()
	if header is not None:
		diffed.cells.insert(0,header)
	print("Generated notebook and autograded")

	if toIpynb:
		save_notebook(diffed,'gradescope')

	if export_notebook(diffed,'gradescope',**kwargs) is not None:
		display(HTML('<h1><a href="gradescope.pdf"> Download this and submit to gradescope!</a></h1>'))
	else:
		display(HTML('<h2>LaTeX failed to parse. Please see error message above</h2>'))




def generateGSTemplate(notebook,location='output'):
	student_notebook = notebook.copy()
	instructor_notebook = notebook.copy()
	diffed = compareThese(instructor_notebook,student_notebook)
	print("Generated template notebook")
	print(diffed.cells)
	export_notebook(diffed,location)

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

def compareThese(nb_base,nb_new):
	"""
		Returns a modified version of nb_new which contains no cells which are
		*similar* to any cells in nb_base

		How similarity is defined depends on implementation; see *similar(cellSource,allOtherCells)*
		for the current implementation
	"""
	allOtherCells = [cell['source'] for cell in nb_base['cells']]
	newCells = [cell for cell in nb_new['cells'] if cell['source'] is not None and (not similar(cell['source'],allOtherCells) \
             or cell['metadata'].get('purpose','NA')=='solution')]

	print("NUM CELLS",len(newCells))
	for cell in newCells:
		execution_num = cell.get('execution_num')
		if 'outputs' in cell:
			if len([i for i in cell['outputs'] if 'data' in i and 'image/png' in i['data']]) > 3:
				print("It looks like you have a cell with 4 or more images")
				print("This may cause errors with the Gradescope submission!")
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
			print("Here's a preview of that cell: %s"%(cell['source'][:100]))
		fix_dollar_sign(cell)

	parse_nb = nb_new.copy()
	parse_nb['cells'] = newCells
	return parse_nb


def similar(cellSource,allOtherCells):
	"""
		Modify this to change how cells are accepted and rejected
	"""
	return (cellSource in allOtherCells and '&zwnj;' not in cellSource)
