Uas as a Python library
================

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

Real-World Examples
-------------------

EPUB Library Analysis
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import os
   from pathlib import Path
   from epub_utils import Document

   def analyze_epub_library(directory):
       """Analyze all EPUB files in a directory."""
       epub_files = Path(directory).glob("*.epub")
       
       results = []
       for epub_path in epub_files:
           try:
               doc = Document(str(epub_path))
               metadata = doc.package.metadata
               
               # Extract key information
               info = {
                   'filename': epub_path.name,
                   'title': getattr(metadata, 'title', 'Unknown'),
                   'author': getattr(metadata, 'creator', 'Unknown'),
                   'language': getattr(metadata, 'language', 'Unknown'),
                   'publisher': getattr(metadata, 'publisher', 'Unknown'),
                   'file_size': epub_path.stat().st_size,
                   'file_count': len(doc.get_files_info())
               }
               results.append(info)
               
           except Exception as e:
               print(f"Error processing {epub_path}: {e}")
       
       return results

   # Usage
   library_info = analyze_epub_library("/path/to/epub/collection")
   
   # Print summary
   for book in library_info:
       print(f"{book['title']} by {book['author']}")
       print(f"  Files: {book['file_count']}, Size: {book['file_size']} bytes")

Metadata Extraction for Cataloging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import csv
   from epub_utils import Document

   def extract_metadata_to_csv(epub_files, output_csv):
       """Extract metadata from multiple EPUB files to CSV."""
       
       fieldnames = [
           'filename', 'title', 'creator', 'publisher', 'date',
           'language', 'identifier', 'subject', 'description'
       ]
       
       with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
           writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
           writer.writeheader()
           
           for epub_file in epub_files:
               try:
                   doc = Document(epub_file)
                   metadata = doc.package.metadata
                   
                   row = {
                       'filename': os.path.basename(epub_file),
                       'title': getattr(metadata, 'title', ''),
                       'creator': getattr(metadata, 'creator', ''),
                       'publisher': getattr(metadata, 'publisher', ''),
                       'date': getattr(metadata, 'date', ''),
                       'language': getattr(metadata, 'language', ''),
                       'identifier': getattr(metadata, 'identifier', ''),
                       'subject': getattr(metadata, 'subject', ''),
                       'description': getattr(metadata, 'description', '')
                   }
                   
                   writer.writerow(row)
                   print(f"Processed: {row['title']}")
                   
               except Exception as e:
                   print(f"Error processing {epub_file}: {e}")

Content Analysis
~~~~~~~~~~~~~~~~

.. code-block:: python

   from epub_utils import Document
   import re

   def analyze_epub_content(epub_path):
       """Analyze content structure and statistics."""
       doc = Document(epub_path)
       
       analysis = {
           'title': getattr(doc.package.metadata, 'title', 'Unknown'),
           'total_files': len(doc.get_files_info()),
           'content_files': 0,
           'total_words': 0,
           'chapters': []
       }
       
       # Find content files
       manifest = doc.package.manifest
       content_items = {
           item_id: item for item_id, item in manifest.items.items()
           if item.get('media-type') == 'application/xhtml+xml'
       }
       
       analysis['content_files'] = len(content_items)
       
       # Analyze each content file
       for content_id, item in content_items.items():
           try:
               # This would require implementing content extraction
               # content = doc.get_content(content_id)
               # word_count = len(content.split())
               # analysis['total_words'] += word_count
               
               chapter_info = {
                   'id': content_id,
                   'file': item['href'],
                   # 'words': word_count
               }
               analysis['chapters'].append(chapter_info)
               
           except Exception as e:
               print(f"Could not analyze content {content_id}: {e}")
       
       return analysis

Integration with Other Libraries
---------------------------------

With BeautifulSoup for HTML Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from epub_utils import Document
   from bs4 import BeautifulSoup
   import zipfile

   def extract_text_with_bs4(epub_path, content_id):
       """Extract clean text using BeautifulSoup."""
       doc = Document(epub_path)
       
       # Get the file path from manifest
       manifest_item = doc.package.manifest.items.get(content_id)
       if not manifest_item:
           raise ValueError(f"Content ID {content_id} not found")
       
       file_path = manifest_item['href']
       
       # Extract content from EPUB
       with zipfile.ZipFile(epub_path, 'r') as epub_zip:
           # Get package directory
           container_path = doc.container.rootfile_path
           package_dir = '/'.join(container_path.split('/')[:-1])
           full_path = f"{package_dir}/{file_path}" if package_dir else file_path
           
           content = epub_zip.read(full_path).decode('utf-8')
           
       # Parse with BeautifulSoup
       soup = BeautifulSoup(content, 'html.parser')
       
       # Extract text
       text = soup.get_text()
       
       # Clean up whitespace
       text = re.sub(r'\s+', ' ', text).strip()
       
       return text

Performance Considerations
--------------------------

Lazy Loading
~~~~~~~~~~~~

epub-utils uses lazy loading to improve performance:

.. code-block:: python

   # Only loads basic file info
   doc = Document("large_book.epub")

   # This triggers parsing of the container
   container = doc.container

   # This triggers parsing of the package
   package = doc.package

   # This triggers parsing of the TOC
   toc = doc.toc

Efficient Batch Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~

For processing many EPUB files:

.. code-block:: python

   import gc
   from epub_utils import Document

   def process_epub_batch(epub_files):
       """Process EPUB files efficiently."""
       for epub_file in epub_files:
           try:
               # Process one file at a time
               doc = Document(epub_file)
               
               # Extract what you need quickly
               title = getattr(doc.package.metadata, 'title', 'Unknown')
               
               # Do your processing
               yield {
                   'file': epub_file,
                   'title': title
               }
               
               # Clean up
               del doc
               gc.collect()
               
           except Exception as e:
               print(f"Error processing {epub_file}: {e}")

Best Practices
--------------

1. **Always use try-except blocks** when working with EPUB files, as they can be malformed
2. **Check for attribute existence** before accessing metadata fields
3. **Use lazy loading** - only access the parts of the EPUB you need
4. **Handle encoding issues** gracefully when working with text content
5. **Consider memory usage** when processing large numbers of files

Next Steps
----------

- Explore the complete :doc:`api-reference` for detailed class documentation
- See more :doc:`examples` for advanced use cases
- Learn about :doc:`epub-standards` to understand the underlying specifications
- Check out the :doc:`cli-reference` for command-line equivalents
