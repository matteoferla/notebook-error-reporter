# Configuration file for the Sphinx documentation builder.
# using commands from https://gist.github.com/matteoferla/ba72ab12a9e5f690277e2e88551773aa
# modified for readthedocs
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# installed in `.readthedocs.yaml`


# -- Project information -----------------------------------------------------

project = 'notebook_error_reporter'
copyright = '2022, MIT licence. Weekend project.'
author = 'Matteo Ferla'
github_username = 'matteoferla'
github_repository = 'remote-notebook-error-collection'


# -- General configuration ---------------------------------------------------

extensions = [
    'readthedocs_ext.readthedocs',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    #'sphinx_toolbox.more_autodoc',
    'sphinx.ext.autodoc',
    #'sphinx.ext.imgconverter',
]

html_static_path = [] # no images.

templates_path = ['_templates']
always_document_param_types = True
typehints_defaults = 'braces'
language = 'en'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = 'sphinx_rtd_theme'
todo_include_todos = True

# --- add init ---------------------------------------------------------

def skip(app, what, name, obj, would_skip, options):
    if name in ( '__init__',):
        return False
    return would_skip

def setup(app):
    app.connect('autodoc-skip-member', skip)

# --- add mk files ---------------------------------------------------------

import m2r2  # noqa
import os, re


repo_base_path = os.path.abspath("../../")

def convert_write(markdown_filename, srt_filename):
    with open(markdown_filename) as fh:
        markdown_block = fh.read()
    markdown_block = re.sub(r"""href=(['"])[./]*images/""", r'href=\1', markdown_block)
    markdown_block = re.sub(r"""src=(['"])[./]*images/""", r'href=\1', markdown_block)

    def fix_md_link(match: re.Match) -> str:
        link = match['link']
        if '../' in link or 'documentation/' in link or 'notes/' in link or 'images/' in link:
            pass
        elif 'documentation' in markdown_filename:  # sibling file
            link = 'doc_' + link
        elif 'notes' in markdown_filename:  # sibling file
            link = 'note_' + link
        link = link.replace('../', '')
        link = re.sub(r'^images/', '_static/', link)
        link = re.sub(r'^documentation/notes/', 'note_', link)
        link = re.sub(r'^documentation/', 'doc_', link)
        link = re.sub(r'^notes/', 'note_', link)
        link = re.sub(r'\.md$', '.html', link)
        return f"[{match['label']}]({link})"

    markdown_block = re.sub(r'\[(?P<label>.*?)\]\((?P<link>.*?)\)', fix_md_link, markdown_block)
    rst_block = m2r2.convert(markdown_block)
    with open(srt_filename, 'w') as fh:
        fh.write(rst_block)

convert_write(os.path.join(repo_base_path, 'README.md'), 'introduction.rst')
