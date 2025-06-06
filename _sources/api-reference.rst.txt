API Reference
=============

This section provides complete API documentation for all classes and methods in epub-utils.

Document Class
--------------

.. py:class:: Document(path)

   Main class for working with EPUB files.

   :param str path: Path to the EPUB file

   **Example**:

   .. code-block:: python

      from epub_utils import Document
      
      doc = Document("book.epub")
      print(doc.package.metadata.title)

   .. py:attribute:: container

      Access to the container information.

      :type: Container
      :returns: Container object with container.xml information

      **Example**:

      .. code-block:: python

         container = doc.container
         print(f"Package path: {container.rootfile_path}")

   .. py:attribute:: package

      Access to the package (OPF) information.

      :type: Package  
      :returns: Package object with OPF file information

      **Example**:

      .. code-block:: python

         package = doc.package
         print(f"Title: {package.metadata.title}")

   .. py:attribute:: toc

      Access to the table of contents.

      :type: TableOfContents
      :returns: Table of contents object

      **Example**:

      .. code-block:: python

         toc = doc.toc
         toc_xml = toc.to_xml()

   .. py:attribute:: ncx

      Access to the NCX (Navigation Control for XML) table of contents.

      :type: TableOfContents or None
      :returns: NCX table of contents object for EPUB 2, or for EPUB 3 if NCX is present, None otherwise

      **Example**:

      .. code-block:: python

         ncx = doc.ncx
         if ncx:
             ncx_xml = ncx.to_xml()

      **Note**: For EPUB 2, this returns the same as ``toc``. For EPUB 3, this specifically 
      accesses the NCX file if present, which provides backward compatibility.

   .. py:attribute:: nav

      Access to the Navigation Document (EPUB 3 only).

      :type: TableOfContents or None
      :returns: Navigation Document table of contents object for EPUB 3, None for EPUB 2 or if not present

      **Example**:

      .. code-block:: python

         nav = doc.nav
         if nav:
             nav_xml = nav.to_xml()

      **Note**: This property specifically accesses EPUB 3 Navigation Documents. 
      Returns None for EPUB 2 documents.

   .. py:method:: get_files_info()

      Get detailed information about all files in the EPUB.

      :returns: List of dictionaries containing file information
      :rtype: List[Dict[str, Union[str, int]]]

      Each dictionary contains:
      - ``path`` (str): File path within the EPUB
      - ``size`` (int): Uncompressed size in bytes  
      - ``compressed_size`` (int): Compressed size in bytes
      - ``modified`` (str): Last modified date in ISO format

      **Example**:

      .. code-block:: python

         files = doc.get_files_info()
         for file_info in files:
             print(f"{file_info['path']}: {file_info['size']} bytes")

   .. py:method:: list_files()

      Get basic information about all files in the EPUB.

      :returns: List of dictionaries with basic file information
      :rtype: List[Dict[str, str]]

      **Example**:

      .. code-block:: python

         files = doc.list_files()
         print(f"EPUB contains {len(files)} files")

Container Class
---------------

.. py:class:: Container

   Represents the META-INF/container.xml file information.

   .. py:attribute:: rootfile_path

      Path to the main package file within the EPUB.

      :type: str

   .. py:attribute:: rootfile_media_type

      Media type of the main package file.

      :type: str

   .. py:method:: to_xml(highlight_syntax=True)

      Get formatted XML representation.

      :param bool highlight_syntax: Whether to apply syntax highlighting
      :returns: Formatted XML string
      :rtype: str

   .. py:method:: to_str()

      Get raw XML content.

      :returns: Raw XML string
      :rtype: str

Package Class
-------------

.. py:class:: Package

   Represents the main OPF package file.

   .. py:attribute:: metadata

      Package metadata information.

      :type: Metadata

   .. py:attribute:: manifest

      Package manifest information.

      :type: Manifest

   .. py:attribute:: spine

      Package spine information.

      :type: Spine

   .. py:method:: to_xml(highlight_syntax=True)

      Get formatted XML representation of the complete package.

      :param bool highlight_syntax: Whether to apply syntax highlighting
      :returns: Formatted XML string
      :rtype: str

   .. py:method:: to_str()

      Get raw XML content of the complete package.

      :returns: Raw XML string
      :rtype: str

Metadata Class
--------------

.. py:class:: Metadata

   Represents Dublin Core and EPUB-specific metadata.

   .. py:attribute:: title

      Book title from dc:title element.

      :type: str

   .. py:attribute:: creator

      Book author/creator from dc:creator element.

      :type: str

   .. py:attribute:: language

      Language code from dc:language element.

      :type: str

   .. py:attribute:: identifier

      Unique identifier from dc:identifier element.

      :type: str

   .. py:attribute:: publisher

      Publisher from dc:publisher element.

      :type: str

   .. py:attribute:: date

      Publication date from dc:date element.

      :type: str

   .. py:attribute:: subject

      Subject/keywords from dc:subject element.

      :type: str

   .. py:attribute:: description

      Description from dc:description element.

      :type: str

   .. py:attribute:: contributor

      Contributor from dc:contributor element.

      :type: str

   .. py:attribute:: type

      Resource type from dc:type element.

      :type: str

   .. py:attribute:: format

      Format from dc:format element.

      :type: str

   .. py:attribute:: source

      Source from dc:source element.

      :type: str

   .. py:attribute:: relation

      Relation from dc:relation element.

      :type: str

   .. py:attribute:: coverage

      Coverage from dc:coverage element.

      :type: str

   .. py:attribute:: rights

      Rights information from dc:rights element.

      :type: str

   .. py:method:: __getattr__(name)

      Dynamic attribute access for any metadata field.

      :param str name: Metadata field name
      :returns: Metadata value or empty string
      :rtype: str

      **Example**:

      .. code-block:: python

         # Access any metadata field
         isbn = metadata.isbn if hasattr(metadata, 'isbn') else 'Not available'
         series = getattr(metadata, 'series', 'Not available')

   .. py:method:: to_xml(highlight_syntax=True)

      Get formatted XML representation of metadata.

      :param bool highlight_syntax: Whether to apply syntax highlighting
      :returns: Formatted XML string
      :rtype: str

   .. py:method:: to_kv()

      Get metadata as key-value pairs.

      :returns: Key-value formatted string
      :rtype: str

      **Example**:

      .. code-block:: python

         kv_data = metadata.to_kv()
         print(kv_data)
         # Output:
         # title: The Great Gatsby
         # creator: F. Scott Fitzgerald
         # language: en

   .. py:method:: to_str()

      Get raw XML content of metadata.

      :returns: Raw XML string
      :rtype: str

Manifest Class
--------------

.. py:class:: Manifest

   Represents the package manifest section.

   .. py:attribute:: items

      Dictionary of manifest items.

      :type: Dict[str, Dict[str, str]]

      Each item contains:
      - ``href``: File path
      - ``media-type``: MIME type
      - Other attributes as needed

      **Example**:

      .. code-block:: python

         for item_id, item in manifest.items.items():
             print(f"ID: {item_id}")
             print(f"  File: {item['href']}")
             print(f"  Type: {item['media-type']}")

   .. py:method:: to_xml(highlight_syntax=True)

      Get formatted XML representation.

      :param bool highlight_syntax: Whether to apply syntax highlighting
      :returns: Formatted XML string
      :rtype: str

   .. py:method:: to_str()

      Get raw XML content.

      :returns: Raw XML string
      :rtype: str

Spine Class
-----------

.. py:class:: Spine

   Represents the package spine section.

   .. py:attribute:: items

      List of spine items in reading order.

      :type: List[Dict[str, str]]

      **Example**:

      .. code-block:: python

         for item in spine.items:
             print(f"Reading order item: {item}")

   .. py:method:: to_xml(highlight_syntax=True)

      Get formatted XML representation.

      :param bool highlight_syntax: Whether to apply syntax highlighting
      :returns: Formatted XML string
      :rtype: str

   .. py:method:: to_str()

      Get raw XML content.

      :returns: Raw XML string
      :rtype: str

TableOfContents Class
---------------------

.. py:class:: TableOfContents

   Represents the table of contents (NCX or Navigation Document).

   .. py:method:: to_xml(highlight_syntax=True)

      Get formatted XML representation.

      :param bool highlight_syntax: Whether to apply syntax highlighting
      :returns: Formatted XML string
      :rtype: str

   .. py:method:: to_str()

      Get raw XML content.

      :returns: Raw XML string
      :rtype: str

Content Classes
---------------

.. py:class:: Content

   Base class for EPUB content documents.

   .. py:method:: to_xml(highlight_syntax=True)

      Get formatted content.

      :param bool highlight_syntax: Whether to apply syntax highlighting
      :returns: Formatted content string
      :rtype: str

   .. py:method:: to_str()

      Get raw content.

      :returns: Raw content string
      :rtype: str

.. py:class:: XHTMLContent

   Specialized class for XHTML content documents.

   Inherits from Content with additional XHTML-specific methods.

   .. py:method:: to_plain()

      Get plain text content with HTML tags stripped.

      :returns: Plain text string
      :rtype: str

      **Example**:

      .. code-block:: python

         from epub_utils.content import XHTMLContent
         
         # This would typically be accessed through Document
         # content = XHTMLContent(raw_html)
         # plain_text = content.to_plain()

Exception Classes
-----------------

.. py:exception:: ParseError

   Raised when there's an error parsing EPUB content.

   Base class: ``Exception``

   **Example**:

   .. code-block:: python

      from epub_utils import Document
      from epub_utils.exceptions import ParseError

      try:
          doc = Document("corrupted.epub")
          title = doc.package.metadata.title
      except ParseError as e:
          print(f"Failed to parse EPUB: {e}")
      except FileNotFoundError:
          print("EPUB file not found")

Usage Examples
--------------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from epub_utils import Document

   # Load document
   doc = Document("book.epub")

   # Access metadata
   metadata = doc.package.metadata
   print(f"Title: {metadata.title}")
   print(f"Author: {metadata.creator}")

   # Check file structure
   files = doc.get_files_info()
   print(f"Contains {len(files)} files")

   # Get formatted output
   toc_xml = doc.toc.to_xml()
   metadata_kv = metadata.to_kv()

Error Handling
~~~~~~~~~~~~~~

.. code-block:: python

   from epub_utils import Document
   from epub_utils.exceptions import ParseError

   def safe_load_epub(path):
       try:
           doc = Document(path)
           return {
               'status': 'success',
               'document': doc,
               'title': getattr(doc.package.metadata, 'title', 'Unknown')
           }
       except ParseError as e:
           return {
               'status': 'parse_error',
               'error': str(e)
           }
       except FileNotFoundError:
           return {
               'status': 'file_not_found',
               'error': 'EPUB file not found'
           }
       except Exception as e:
           return {
               'status': 'unknown_error', 
               'error': str(e)
           }

Batch Processing
~~~~~~~~~~~~~~~~

.. code-block:: python

   import os
   from pathlib import Path
   from epub_utils import Document

   def process_epub_directory(directory):
       epub_files = Path(directory).glob("*.epub")
       results = []
       
       for epub_path in epub_files:
           try:
               doc = Document(str(epub_path))
               metadata = doc.package.metadata
               
               result = {
                   'file': epub_path.name,
                   'title': getattr(metadata, 'title', ''),
                   'author': getattr(metadata, 'creator', ''),
                   'language': getattr(metadata, 'language', ''),
                   'file_size': epub_path.stat().st_size,
                   'epub_files': len(doc.get_files_info())
               }
               results.append(result)
               
           except Exception as e:
               results.append({
                   'file': epub_path.name,
                   'error': str(e)
               })
       
       return results

Type Hints
----------

For better IDE support and type checking, here are the main type hints:

.. code-block:: python

   from typing import Dict, List, Union, Optional
   from epub_utils import Document

   # Function signatures for reference
   def get_files_info(self) -> List[Dict[str, Union[str, int]]]: ...
   def list_files(self) -> List[Dict[str, str]]: ...
   def to_xml(self, highlight_syntax: bool = True) -> str: ...
   def to_str(self) -> str: ...
   def to_kv(self) -> str: ...

   # Type-safe usage example
   doc: Document = Document("book.epub")
   files_info: List[Dict[str, Union[str, int]]] = doc.get_files_info()
   title: str = doc.package.metadata.title
   kv_data: str = doc.package.metadata.to_kv()

Module Structure
----------------

The ``epub-utils`` package is organized as follows:

.. code-block:: text

   epub_utils/
   ├── __init__.py          # Main exports (Document, Container)
   ├── doc.py               # Document class
   ├── container.py         # Container class
   ├── package/
   │   ├── __init__.py      # Package class
   │   ├── metadata.py      # Metadata class
   │   ├── manifest.py      # Manifest class
   │   └── spine.py         # Spine class
   ├── content/
   │   ├── __init__.py      # Content classes
   │   ├── base.py          # Base Content class
   │   └── xhtml.py         # XHTMLContent class
   ├── toc.py               # TableOfContents class
   ├── exceptions.py        # Exception classes
   ├── highlighters.py      # Syntax highlighting utilities
   └── cli.py               # Command-line interface

For detailed implementation examples, see :doc:`api-tutorial` and :doc:`examples`.
