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

We use the following structure inside the IPython notebook in order to correctly work

- If a markdown cell contains '#newpage' in the source, this cell is added no matter what: a 2 pagebreak is added prior to the markdown cell (this will align every 2 pages) 
- If a cell's metadata has cell['metadata']['#student'] = True, then the cell is added no matter what
- We need a list of MD5 checksums of each cell  in the notebook metadata: nb['metadata]['checksums']



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