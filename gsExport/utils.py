import nbformat as nbf
import nbconvert
from nbconvert import PDFExporter
import pkg_resources
import shutil

def load_notebook(name):
	return nbf.read(name,nbf.current_nbformat)

def save_notebook(nb,name):
	nbf.write(nb,open("%s.ipynb"%name,"w"))

def export_notebook(nb,name,templating="test.tplx",debug=False):
	shutil.copyfile(pkg_resources.resource_filename(__name__,templating),"test.tplx")
	pdf_exporter = PDFExporter()
	pdf_exporter.template_file ="test.tplx"
	print("Attempting to compile LaTeX")
	try:
		pdf_output = pdf_exporter.from_notebook_node(nb)
		with open("%s.pdf"%name,"wb") as output_file:
			output_file.write(pdf_output[0])
			print("Finished generating PDF")
	except nbconvert.pdf.LatexFailed as error:
		print("There was an error generating your LaTeX")
		if debug:
			print("Showing full error message from PDFTex")
			print("="*30)
			print(error.output)
			print("="*30)

		else:
			print("Showing concise error message")
			print("="*30)
			print('\n'.join(error.output.split('\n')[-15:]))
			print("="*30)
		return None
	return "%s.pdf"%name


def run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False
