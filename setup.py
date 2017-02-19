
import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "gsExport",
    version = "0.2.1",
    author = "Dibya Ghosh",
    author_email = "dibya@berkeley.edu",
    description = ("A set of utilities to expedite submission of jupyter notebooks to Gradescope"),
    license = "BSD",
    keywords = "gradescope jupyter notebook pdf submission latex export",
    url = "http://packages.python.org/gsExport",
    packages=['gsExport'],
    long_description=read("README.rst"),
    install_requires = ['pytz','jupyter','notebook','nbformat','nbconvert<5','okpy','tqdm'],
    package_data={'gsExport': ['*.tplx']},    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
