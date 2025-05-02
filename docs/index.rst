epub-utils
==========

A Python CLI and utility library for manipulating EPUB files.

.. image:: https://img.shields.io/pypi/v/epub-utils.svg
   :target: https://pypi.org/project/epub-utils/
   :alt: PyPI version

.. image:: https://img.shields.io/badge/license-Apache%202.0-blue.svg
   :target: https://github.com/ernestofgonzalez/epub-utils/blob/main/LICENSE
   :alt: License

epub-utils is a Python library and command-line tool that helps you inspect and manipulate EPUB files.
It provides both a programmatic API and a CLI interface for working with EPUB metadata, content, and structure.

Features
--------

- Parse and validate EPUB container and package files
- Extract metadata like title, author, and identifier
- Command-line interface for quick file inspection
- Syntax highlighted XML output

Installation
------------

To install epub-utils, run:

.. code-block:: bash

    pip install epub-utils

Quick Start
----------

Command Line Usage
~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Show container.xml contents
    epub-utils your-book.epub container

    # Show package OPF contents with syntax highlighting
    epub-utils your-book.epub package

    # Show table of contents
    epub-utils your-book.epub toc

Python Library Usage
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from epub_utils import Document

    # Load an EPUB document
    doc = Document("path/to/book.epub")

    # Access container metadata
    print(f"Package file location: {doc.container.rootfile_path}")

    # Access package metadata
    print(f"Title: {doc.package.title}")
    print(f"Author: {doc.package.author}")
    print(f"Identifier: {doc.package.identifier}")