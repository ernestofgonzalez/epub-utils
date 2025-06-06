Use as a Python library
=======================

This guide covers using ``epub-utils`` as a Python library. The API is designed to be intuitive 
and follows Python best practices for ease of use and integration into your projects.

Quick Start
-----------

The main entry point is the ``Document`` class:

.. code-block:: python

   from epub_utils import Document

   # Load an EPUB file
   doc = Document("path/to/book.epub")

   # Access various components
   print(f"Title: {doc.package.metadata.title}")
   print(f"Author: {doc.package.metadata.creator}")

Core Classes
------------

Document Class
~~~~~~~~~~~~~~

The ``Document`` class is your main interface to an EPUB file:

.. code-block:: python

   from epub_utils import Document

   doc = Document("example.epub")

   # Access major components
   container = doc.container      # Container information
   package = doc.package         # Package/OPF file
   toc = doc.toc                 # Table of contents
   
   # Get file information
   files_info = doc.get_files_info()

**Key Methods**:

- ``get_files_info()``: Returns detailed information about all files in the EPUB
- ``list_files()``: Returns a simple list of files with basic metadata

Container Access
~~~~~~~~~~~~~~~~

The container provides information from the META-INF/container.xml file:

.. code-block:: python

   # Access container properties
   print(f"Package path: {doc.container.rootfile_path}")
   print(f"Media type: {doc.container.rootfile_media_type}")

   # Get raw XML
   container_xml = doc.container.to_xml()
   raw_container = doc.container.to_str()

Package and Metadata
~~~~~~~~~~~~~~~~~~~~~

The package object gives you access to the main OPF file and its metadata:

.. code-block:: python

   package = doc.package

   # Access metadata
   metadata = package.metadata
   print(f"Title: {metadata.title}")
   print(f"Author: {metadata.creator}")
   print(f"Language: {metadata.language}")
   print(f"Identifier: {metadata.identifier}")
   print(f"Publisher: {metadata.publisher}")

   # Get all metadata as key-value pairs
   kv_metadata = metadata.to_kv()
   print(kv_metadata)

   # Access manifest and spine
   manifest = package.manifest
   spine = package.spine

Working with Metadata
----------------------

Extracting Common Fields
~~~~~~~~~~~~~~~~~~~~~~~~~

The metadata object provides easy access to Dublin Core and EPUB-specific metadata:

.. code-block:: python

   metadata = doc.package.metadata

   # Basic Dublin Core elements
   title = metadata.title
   creator = metadata.creator  # Usually the author
   subject = metadata.subject  # Keywords/topics
   description = metadata.description
   publisher = metadata.publisher
   contributor = metadata.contributor
   date = metadata.date
   type = metadata.type
   format = metadata.format
   identifier = metadata.identifier
   source = metadata.source
   language = metadata.language
   relation = metadata.relation
   coverage = metadata.coverage
   rights = metadata.rights

Dynamic Attribute Access
~~~~~~~~~~~~~~~~~~~~~~~~

The metadata object supports dynamic attribute access for any metadata field:

.. code-block:: python

   # Access any metadata field by name
   isbn = getattr(metadata, 'isbn', 'Not available')
   series = getattr(metadata, 'series', 'Not available')

   # Or use the more direct approach
   try:
       custom_field = metadata.custom_metadata_field
   except AttributeError:
       custom_field = "Field not found"

Formatted Output
~~~~~~~~~~~~~~~~

Get metadata in different formats:

.. code-block:: python

   # XML format with syntax highlighting
   xml_metadata = metadata.to_xml(highlight_syntax=True)

   # Raw XML without highlighting
   raw_xml = metadata.to_xml(highlight_syntax=False)

   # Key-value format for easy parsing
   kv_format = metadata.to_kv()

Manifest and Spine
-------------------

Working with the Manifest
~~~~~~~~~~~~~~~~~~~~~~~~~~

The manifest lists all files in the EPUB package:

.. code-block:: python

   manifest = doc.package.manifest

   # Get all items
   items = manifest.items  # Dictionary of manifest items

   # Find specific items
   for item_id, item in items.items():
       print(f"ID: {item_id}")
       print(f"  File: {item['href']}")
       print(f"  Type: {item['media-type']}")

   # Get formatted output
   manifest_xml = manifest.to_xml()

Understanding the Spine
~~~~~~~~~~~~~~~~~~~~~~~~

The spine defines the reading order:

.. code-block:: python

   spine = doc.package.spine

   # Get spine items in reading order
   spine_items = spine.items

   # Get formatted output
   spine_xml = spine.to_xml()

Table of Contents
-----------------

Working with TOC
~~~~~~~~~~~~~~~~

Access the table of contents (either NCX or Navigation Document):

.. code-block:: python

   toc = doc.toc

   # Get formatted TOC
   toc_xml = toc.to_xml()
   raw_toc = toc.to_str()

Specific TOC Access
~~~~~~~~~~~~~~~~~~~

For fine-grained control over which table of contents format to access:

.. code-block:: python

   # Access NCX specifically (EPUB 2 or EPUB 3 with NCX)
   ncx = doc.ncx
   if ncx:
       ncx_xml = ncx.to_xml()
       print("NCX navigation available")
   else:
       print("No NCX navigation found")

   # Access Navigation Document specifically (EPUB 3 only)
   nav = doc.nav
   if nav:
       nav_xml = nav.to_xml()
       print("Navigation Document available")
   else:
       print("No Navigation Document found (likely EPUB 2)")

   # Handle different EPUB versions
   package = doc.package
   if package.version.major >= 3:
       # EPUB 3 - prefer Navigation Document, fallback to NCX
       nav_doc = doc.nav or doc.ncx
   else:
       # EPUB 2 - use NCX
       nav_doc = doc.ncx

   if nav_doc:
       print("Table of contents found:", nav_doc.to_str()[:100])

Content Extraction
------------------

Accessing Document Content
~~~~~~~~~~~~~~~~~~~~~~~~~~

Extract content from specific documents within the EPUB:

.. code-block:: python

   # First, find content IDs from the manifest
   manifest = doc.package.manifest
   content_items = {
       item_id: item for item_id, item in manifest.items.items()
       if item['media-type'] == 'application/xhtml+xml'
   }

   # Access content by ID
   for content_id in content_items:
       try:
           content = doc.get_content(content_id)
           # Process content as needed
           print(f"Content ID {content_id}: {len(content)} characters")
       except Exception as e:
           print(f"Could not access content {content_id}: {e}")

File Information
----------------

Detailed File Analysis
~~~~~~~~~~~~~~~~~~~~~~

Get comprehensive information about all files in the EPUB:

.. code-block:: python

   files_info = doc.get_files_info()

   for file_info in files_info:
       print(f"Path: {file_info['path']}")
       print(f"Size: {file_info['size']} bytes")
       print(f"Compressed: {file_info['compressed_size']} bytes")
       print(f"Modified: {file_info['modified']}")
       print("---")

   # Calculate total size
   total_size = sum(f['size'] for f in files_info)
   total_compressed = sum(f['compressed_size'] for f in files_info)
   compression_ratio = (1 - total_compressed / total_size) * 100
   
   print(f"Total size: {total_size} bytes")
   print(f"Compressed size: {total_compressed} bytes")
   print(f"Compression ratio: {compression_ratio:.1f}%")

Error Handling
--------------

Robust Error Handling
~~~~~~~~~~~~~~~~~~~~~~

epub-utils provides specific exception types for better error handling:

.. code-block:: python

   from epub_utils import Document
   from epub_utils.exceptions import ParseError

   try:
       doc = Document("potentially_corrupt.epub")
       
       # Try to access metadata
       title = doc.package.metadata.title
       print(f"Successfully loaded: {title}")
       
   except ParseError as e:
       print(f"EPUB parsing error: {e}")
   except FileNotFoundError:
       print("EPUB file not found")
   except Exception as e:
       print(f"Unexpected error: {e}")

Graceful Degradation
~~~~~~~~~~~~~~~~~~~~

Handle missing or malformed metadata gracefully:

.. code-block:: python

   def safe_get_metadata(doc, field_name, default="Unknown"):
       """Safely extract metadata field with fallback."""
       try:
           return getattr(doc.package.metadata, field_name, default)
       except (AttributeError, ParseError):
           return default

   # Usage
   title = safe_get_metadata(doc, 'title', 'Untitled')
   author = safe_get_metadata(doc, 'creator', 'Unknown Author')

Next Steps
----------

- Explore the complete :doc:`api-reference` for detailed class documentation
- See more :doc:`examples` for advanced use cases
- Learn about :doc:`epub-standards` to understand the underlying specifications
- Check out the :doc:`cli-reference` for command-line equivalents
