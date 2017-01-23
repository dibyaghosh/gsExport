# gsExport

**gsExport** is a utility designed to help educators simplify and streamline the process of grading student notebooks. Designed to alleviate the struggles realized in UC Berkeley's *Data 8*, the system allows students to easily export Jupyter notebooks as PDFs which are segmented to allow for easy grading through the Gradescope interface.

## Features

The system is easy to use, once installed on the client computer.

In order to generate the PDF file, students simply run the following commands

	import gsExport
	gsExport.generateSubmission()


The exporting tool does the following:

- Using the OK autograder in the current directory, it grades the current kernel and generates a table for easy access on Gradescope
- We diff the student's notebook with the default "beginning" notebook, to see what regions students actually contributed to. By doing so, we eliminate a lot of the text/in-place code which doesn't need to be graded
- Using a custom LaTex template, we 


## Structure Requirements

 We require a default directory structure (however, this can easily be modified) as following


- *.ok file (the OK file which we do autograding from)
- tests/  (A folder containing all the relevant tests for autograding)
- grading/ (A folder in which we store the base version of the notebook - used for diffing and generating the notebook)
- *.ipynb (the student's Ipython notebook file)


## Installation

	pip install gsExport# Not yet uploaded
	pip install git+git://github.com/dibyaghosh/gsExport


## Development

- **exporter.py** - contains the main logic for the exporter
- **utils.py** - contains utilities for importing and exporting notebooks
- **ok_grading.py** - contains the OK autograder and export logic


#### For those interested in bundling files

See **setup.py** for the commands required to install bundled files
See **utils.py** for the commands required to fetch the bundled files (this is actually quite jank right now, because of a weird bug with *Jupyter nbConvert* )