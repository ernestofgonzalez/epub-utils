Use as a command-line tool
============

This tutorial will guide you through using ``epub-utils`` from the command line. We'll cover all 
available commands with practical examples and tips for everyday usage.

Getting Started
---------------

The basic syntax for epub-utils is:

.. code-block:: bash

   epub-utils [OPTIONS] EPUB_FILE COMMAND [COMMAND_OPTIONS]

Let's start with a simple example:

.. code-block:: bash

   # Display help
   epub-utils --help

   # Check version
   epub-utils --version

Basic File Inspection
---------------------

Container Information
~~~~~~~~~~~~~~~~~~~~~

The container command shows the EPUB's container.xml file, which points to the main package file:

.. code-block:: bash

   # Show container with syntax highlighting (default)
   epub-utils book.epub container

   # Show raw XML without highlighting
   epub-utils book.epub container --format raw

**Example output**:

.. code-block:: xml

   <?xml version="1.0" encoding="UTF-8"?>
   <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
     <rootfiles>
       <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
     </rootfiles>
   </container>

Package Information
~~~~~~~~~~~~~~~~~~~

The package command displays the main OPF (Open Packaging Format) file:

.. code-block:: bash

   # Show package file with highlighting
   epub-utils book.epub package

   # Show raw package content
   epub-utils book.epub package --format raw

This reveals the complete EPUB structure including metadata, manifest, and spine.

Working with Metadata
----------------------

Extracting Metadata
~~~~~~~~~~~~~~~~~~~~

The metadata command is perfect for getting book information:

.. code-block:: bash

   # Pretty-printed metadata with highlighting
   epub-utils book.epub metadata

   # Key-value format for scripting
   epub-utils book.epub metadata --format kv

**Example key-value output**:

.. code-block:: text

   title: The Great Gatsby
   creator: F. Scott Fitzgerald
   language: en
   identifier: urn:uuid:12345678-1234-1234-1234-123456789abc
   publisher: Scribner
   date: 2021-01-01
   subject: Fiction, Classic Literature

Scripting with Metadata
~~~~~~~~~~~~~~~~~~~~~~~~

The key-value format is perfect for shell scripting:

.. code-block:: bash

   # Extract just the title
   epub-utils book.epub metadata --format kv | grep "^title:" | cut -d' ' -f2-

   # Get author name
   author=$(epub-utils book.epub metadata --format kv | grep "^creator:" | cut -d' ' -f2-)
   echo "Author: $author"

   # Batch process multiple files
   for epub in *.epub; do
       title=$(epub-utils "$epub" metadata --format kv | grep "^title:" | cut -d' ' -f2-)
       echo "$epub: $title"
   done

Understanding EPUB Structure
-----------------------------

Table of Contents
~~~~~~~~~~~~~~~~~

View the navigation structure of your EPUB:

.. code-block:: bash

   # Show table of contents with highlighting
   epub-utils book.epub toc

   # Raw TOC for processing
   epub-utils book.epub toc --format raw

Manifest Inspection
~~~~~~~~~~~~~~~~~~~

The manifest lists all files contained in the EPUB:

.. code-block:: bash

   # View manifest with syntax highlighting
   epub-utils book.epub manifest

   # Raw manifest content
   epub-utils book.epub manifest --format raw

**What you'll see**: Each item in the manifest includes:
- ``id``: Unique identifier for the item
- ``href``: File path within the EPUB
- ``media-type``: MIME type of the file

Spine Information
~~~~~~~~~~~~~~~~~

The spine defines the reading order of the book:

.. code-block:: bash

   # View spine with highlighting
   epub-utils book.epub spine

   # Raw spine for processing
   epub-utils book.epub spine --format raw

Content Extraction
------------------

Viewing Document Content
~~~~~~~~~~~~~~~~~~~~~~~~

Extract content from specific documents using their manifest ID:

.. code-block:: bash

   # Show content with syntax highlighting
   epub-utils book.epub content chapter1

   # Raw HTML/XHTML content
   epub-utils book.epub content chapter1 --format raw

   # Plain text (HTML tags stripped)
   epub-utils book.epub content chapter1 --format plain

**Finding Content IDs**: Use the manifest command to see available content IDs:

.. code-block:: bash

   # First, check the manifest for available IDs
   epub-utils book.epub manifest

   # Then extract specific content
   epub-utils book.epub content intro --format plain

File Listing
~~~~~~~~~~~~

Get detailed information about all files in the EPUB:

.. code-block:: bash

   # Formatted table of files
   epub-utils book.epub files

   # Raw file list
   epub-utils book.epub files --format raw

Advanced Usage Patterns
------------------------

Quality Assurance Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check EPUB files for common issues:

.. code-block:: bash

   #!/bin/bash
   # epub-check.sh - Basic EPUB validation script

   epub_file="$1"

   if [ ! -f "$epub_file" ]; then
       echo "Usage: $0 <epub-file>"
       exit 1
   fi

   echo "=== Checking $epub_file ==="

   # Check if container is valid
   echo "Container structure:"
   epub-utils "$epub_file" container --format raw > /dev/null
   if [ $? -eq 0 ]; then
       echo "✓ Container is valid"
   else
       echo "✗ Container has issues"
   fi

   # Check metadata
   echo -e "\nMetadata:"
   epub-utils "$epub_file" metadata --format kv | head -5

   # Check file count
   file_count=$(epub-utils "$epub_file" files --format raw | wc -l)
   echo -e "\nFile count: $file_count files"

Batch Processing
~~~~~~~~~~~~~~~~

Process multiple EPUB files efficiently:

.. code-block:: bash

   #!/bin/bash
   # batch-epub-info.sh - Extract info from multiple EPUBs

   echo "filename,title,author,language,files" > epub_info.csv

   for epub in *.epub; do
       if [ -f "$epub" ]; then
           # Extract metadata
           metadata=$(epub-utils "$epub" metadata --format kv)
           title=$(echo "$metadata" | grep "^title:" | cut -d' ' -f2- | tr ',' ';')
           author=$(echo "$metadata" | grep "^creator:" | cut -d' ' -f2- | tr ',' ';')
           language=$(echo "$metadata" | grep "^language:" | cut -d' ' -f2-)
           
           # Count files
           file_count=$(epub-utils "$epub" files --format raw | wc -l)
           
           echo "$epub,$title,$author,$language,$file_count" >> epub_info.csv
       fi
   done

   echo "Results saved to epub_info.csv"

Content Analysis
~~~~~~~~~~~~~~~~

Analyze EPUB content structure:

.. code-block:: bash

   #!/bin/bash
   # analyze-content.sh - Analyze EPUB content structure

   epub_file="$1"

   echo "=== Content Analysis for $epub_file ==="

   # Get all content files from manifest
   epub-utils "$epub_file" manifest --format raw | \
   grep 'media-type="application/xhtml+xml"' | \
   sed 's/.*id="\([^"]*\)".*/\1/' | \
   while read -r content_id; do
       echo "--- Content ID: $content_id ---"
       word_count=$(epub-utils "$epub_file" content "$content_id" --format plain | wc -w)
       echo "Word count: $word_count"
       echo ""
   done

Output Format Options
---------------------

epub-utils supports multiple output formats for different use cases:

XML Format (Default)
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   epub-utils book.epub metadata
   # Produces syntax-highlighted, formatted XML

Raw Format
~~~~~~~~~~

.. code-block:: bash

   epub-utils book.epub metadata --format raw
   # Produces unformatted XML, perfect for piping to other tools

Key-Value Format
~~~~~~~~~~~~~~~~

.. code-block:: bash

   epub-utils book.epub metadata --format kv
   # Produces key: value pairs, ideal for scripting

Plain Text Format
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   epub-utils book.epub content chapter1 --format plain
   # Strips HTML tags, produces readable text

Integration Examples
--------------------

With jq (JSON processing)
~~~~~~~~~~~~~~~~~~~~~~~~~

While ``epub-utils`` doesn't output JSON directly, you can convert key-value output:

.. code-block:: bash

   # Convert metadata to JSON-like format
   epub-utils book.epub metadata --format kv | \
   sed 's/^\([^:]*\): \(.*\)$/"\1": "\2",/' | \
   sed '$s/,$//' | \
   (echo "{"; cat; echo "}")

With xmllint (XML validation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Validate XML structure
   epub-utils book.epub package --format raw | xmllint --format --valid -

   # Pretty-print without epub-utils highlighting
   epub-utils book.epub toc --format raw | xmllint --format -

Performance Tips
----------------

1. **Use raw format for large files**: When processing many files, use ``--format raw`` to avoid syntax highlighting overhead.

2. **Pipe efficiently**: Chain commands effectively:

   .. code-block:: bash

      epub-utils book.epub manifest --format raw | grep "\.html" | wc -l

3. **Cache results**: For repeated operations, save output to temporary files:

   .. code-block:: bash

      epub-utils book.epub metadata --format kv > /tmp/metadata.txt
      # Process /tmp/metadata.txt multiple times

Troubleshooting Common Issues
-----------------------------

File Not Found
~~~~~~~~~~~~~~

.. code-block:: bash

   epub-utils: Error: Invalid value for 'PATH': File 'book.epub' does not exist.

**Solution**: Check the file path and ensure the EPUB file exists.

Invalid EPUB Structure
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   epub-utils book.epub container
   # ParseError: Unable to parse container.xml

**Solution**: The EPUB file may be corrupted. Try:

.. code-block:: bash

   # Check if it's a valid ZIP file
   unzip -t book.epub

   # Extract and examine manually
   unzip book.epub -d temp/
   ls temp/

Content ID Not Found
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   epub-utils book.epub content nonexistent
   # Error: Content with id 'nonexistent' not found

**Solution**: Check available content IDs first:

.. code-block:: bash

   epub-utils book.epub manifest | grep 'id='

Next Steps
----------

Now that you're familiar with the CLI basics, you might want to:

- Explore the :doc:`api-tutorial` for programmatic access
- Check out more :doc:`examples` for real-world use cases
- Learn about :doc:`epub-standards` for deeper understanding
- Contribute to the project via :doc:`contributing`
