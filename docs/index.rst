epub-utils: EPUB Inspection and Manipulation
=============================================

.. image:: https://img.shields.io/pypi/v/epub-utils.svg
   :target: https://pypi.org/project/epub-utils/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/epub-utils.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/epub-utils/
   :alt: Python versions

.. image:: https://img.shields.io/badge/license-Apache%202.0-blue.svg
   :target: https://github.com/ernestofgonzalez/epub-utils/blob/main/LICENSE
   :alt: License

**epub-utils** is a comprehensive Python library and command-line tool for working with EPUB files. 
It provides both a programmatic API and an intuitive CLI interface for inspecting, parsing, and 
manipulating EPUB metadata, content, and structure.

.. note::
   epub-utils supports **EPUB 2.0.1** and **EPUB 3.0+** specifications, ensuring compatibility 
   with the vast majority of EPUB files in circulation.

Key Features
------------

✨ **Rich CLI Interface**
   - Syntax-highlighted XML output
   - Multiple output formats (XML, raw, key-value, plain text)
   - Comprehensive file inspection capabilities

📚 **Complete EPUB Support**
   - Parse container.xml and package files
   - Extract and display table of contents
   - Access manifest and spine information
   - Retrieve document content by ID

🔍 **Metadata Extraction**
   - Dublin Core metadata support
   - EPUB-specific metadata fields
   - Key-value output for easy parsing

🐍 **Python API**
   - Clean, object-oriented interface
   - Lazy loading for performance
   - Comprehensive error handling

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   $ pip install epub-utils

Basic CLI Usage
~~~~~~~~~~~~~~~

Inspect an EPUB file with a simple command:

.. code-block:: bash

   # Display metadata with beautiful syntax highlighting
   $ epub-utils my-book.epub metadata

   # Show table of contents structure
   $ epub-utils my-book.epub toc

   # Get key-value metadata for scripting
   $ epub-utils my-book.epub metadata --format kv

Basic Python Usage
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from epub_utils import Document

   # Load an EPUB document
   doc = Document("path/to/book.epub")

   # Access metadata easily
   print(f"Title: {doc.package.metadata.title}")
   print(f"Author: {doc.package.metadata.creator}")
   print(f"Language: {doc.package.metadata.language}")

   # Get table of contents
   toc_xml = doc.toc.to_xml()
   print(toc_xml)

Why epub-utils?
---------------

epub-utils fills a crucial gap in the Python ecosystem for EPUB file manipulation. While there are 
libraries for creating EPUBs, few focus on inspection and analysis. This tool is perfect for:

   **Publishers and Authors**
   Validate EPUB structure and metadata before distribution

   **Digital Librarians**
   Batch process and analyze EPUB collections

   **Automation Scripts**
   Extract metadata for catalogs and databases

   **Debugging**
   Inspect malformed or problematic EPUB files

   **Learning**
   Understand EPUB structure and standards compliance

Real-World Examples
-------------------

**Scenario 1: Batch Metadata Extraction**

.. code-block:: bash

   # Extract titles from all EPUB files in a directory
   for epub in *.epub; do
       echo "$epub: $(epub-utils "$epub" metadata --format kv | grep 'title:')"
   done

**Scenario 2: Content Analysis**

.. code-block:: python

   from epub_utils import Document
   import os

   # Analyze all EPUBs in a directory
   for filename in os.listdir('/path/to/epub/collection'):
       if filename.endswith('.epub'):
           doc = Document(filename)
           print(f"{filename}:")
           print(f"  Title: {doc.package.metadata.title}")
           print(f"  Files: {len(doc.package.manifest.items)} items")
           print(f"  Size: {os.path.getsize(filename)} bytes")

**Scenario 3: Quality Assurance**

.. code-block:: bash

   # Validate EPUB structure
   epub-utils suspicious-book.epub container
   epub-utils suspicious-book.epub package --format raw | xmllint --format -

Documentation Contents
----------------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   cli-tutorial
   api-tutorial
   examples
   formats

.. toctree::
   :maxdepth: 2
   :caption: Reference

   cli-reference
   api-reference
   epub-standards

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing
   changelog

Community & Support
-------------------

- **Source Code**: `GitHub Repository <https://github.com/ernestofgonzalez/epub-utils>`_
- **Issues**: `Bug Reports & Feature Requests <https://github.com/ernestofgonzalez/epub-utils/issues>`_
- **PyPI**: `Package Index <https://pypi.org/project/epub-utils/>`_

License
-------

epub-utils is distributed under the `Apache License 2.0 <https://github.com/ernestofgonzalez/epub-utils/blob/main/LICENSE>`_.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`