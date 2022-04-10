__version__ = '0.1'

from setuptools import setup, find_packages

from warnings import warn
from importlib import util
import sys, os
from setuptools import setup, find_packages

# ---------- Setup  ------------------------------------------------------------------------------------------

import os

this_directory = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(this_directory, 'requirements.txt'), 'r') as fh:
        requirements = [line.strip() for line in fh.read().split() if line and '#' not in line]
    with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        __doc__ = f.read()
except Exception:  # weird file
    requirements = []
    __doc__ = ''

description = 'A error notification system for remote Jupyter notebooks'

setup(
    name='pyrosetta_help',
    version=__version__,
    python_requires='>=3.7',
    packages=find_packages(),
    install_requires=requirements,
    extras_require={'server': ['uvicorn', 'fastapi', 'databases', 'pydantic', 'sqlalchemy']},
    url='https://github.com/matteoferla/remote-notebook-error-collection',
    license='MIT',
    author='Matteo Ferla',
    author_email='matteo.ferla@gmail.com',
    classifiers=[  # https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',  # Development Status :: 5 - Production/Stable
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Chemistry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description=description,
    long_description=__doc__,
    long_description_content_type='text/markdown',
)
