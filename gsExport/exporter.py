import nbformat as nbf
from nbconvert import PDFExporter
import os
import glob
from IPython.core.display import display, HTML
from . import ok_grading
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

def generateSubmission():
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
	diffed.cells.insert(0,ok_grading.autograde_ipython())
	print("Generated notebook and autograded")

	export_notebook(diffed,'gradescope')
	display(HTML('<h1><a href="gradescope.pdf"> Download this and submit to gradescope!</a></h1>'))



def compareThese(nb_base,nb_new):
	"""
		Returns a modified version of nb_new which contains no cells which are 
		*similar* to any cells in nb_base

		How similarity is defined depends on implementation; see *similar(cellSource,allOtherCells)*
		for the current implementation
	"""
	allOtherCells = [cell['source'] for cell in nb_base['cells']]
	newCells = [cell for cell in nb_new['cells'] if not similar(cell['source'],allOtherCells)]
	for cell in newCells:
		if 'outputs' in cell and \
		len([i for i in cell['outputs'] if 'data' in i and 'image/png' in i['data']]) > 3:
			print("It looks like you have a cell with 4 or more images")
			print("This may cause errors with the Gradescope submission!")
	parse_nb = nb_new.copy()
	parse_nb['cells'] = newCells
	return parse_nb


def similar(cellSource,allOtherCells):
	"""
		Modify this to change how cells are accepted and rejected
	"""
	return cellSource in allOtherCells and '**Question' not in cellSource
