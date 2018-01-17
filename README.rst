gsExport
========

**gsExport** is a utility designed to help educators simplify and
streamline the process of grading student notebooks. Designed to
alleviate the struggles realized in UC Berkeley’s *Data 8*, the system
allows students to easily export Jupyter notebooks as PDFs which are
segmented to allow for easy grading through the Gradescope interface.

Features
--------

The system is easy to use, once installed on the client computer.

In order to generate the PDF file for a notebook, students simply run the following
commands

::

    import gsExport
    gsExport.generateSubmission("hw01a.ipynb")


The exporting tool does the following:


-  We diff the student’s notebook with the default “beginning” notebook,
   to see what regions students actually contributed to. By doing so, we
   eliminate a lot of the text/in-place code which doesn’t need to be
   graded
-  Using a custom LaTex template, we export to PDF (with pagebreaks as necessary)

Structure Requirements
----------------------

How to work with gsExport

In your notebook, add the following

- add the text `#newpage` in the Markdown cells before which you'd like to pagebreak (for example, the beginning of a question)
- add '#student' on all cells in which you expect the student to write information

To generate the new notebook, run the following commands in the shell

::

    jupyter nbconvert hw01a.ipynb --NotebookExporter.preprocessors="['gsExport.gsExportPreprocessor']" --to notebook 

which will generate a notebook with all the appropriate structure in hw01a.nbconvert.ipynb. The following structure inside the IPython notebook is added

- The number of '#newpages' in nb['metadata']['number_of_pages']
- All cells with '#student' set cell['metadata']['#student'] = True, and the line with '#student' is removed
- We save a list of MD5 checksums of each cell  in the notebook metadata: nb['metadata]['checksums']



Installation
------------

::

    pip install gsExport
    pip install git+git://github.com/dibyaghosh/gsExport # alternatively

Development
-----------

-  **exporter.py** - contains the main logic for the exporter
-  **utils.py** - contains utilities for importing and exporting
   notebooks
-  **ok\_grading.py** - contains the OK autograder and export logic

For those interested in bundling files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See **setup.py** for the commands required to install bundled files See
**utils.py** for the commands required to fetch the bundled files (this
is actually quite jank right now, because of a weird bug with *Jupyter
nbConvert* )