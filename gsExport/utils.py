import nbformat as nbf
from nbconvert import PDFExporter
import pkg_resources
import shutil

def load_notebook(name):
	return nbf.read(name,nbf.current_nbformat)

def save_notebook(nb,name):
	nbf.write(nb,open("%s.ipynb"%name,"w"))

def export_notebook(nb,name,templating="test.tplx"):
	shutil.copyfile(pkg_resources.resource_filename(__name__,templating),"test.tplx")
	pdf_exporter = PDFExporter()
	pdf_exporter.template_file ="test.tplx"
	pdf_output = pdf_exporter.from_notebook_node(nb)
	with open("%s.pdf"%name,"wb") as output_file:
		output_file.write(pdf_output[0])
		print("Finished generating PDF")


def run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False
