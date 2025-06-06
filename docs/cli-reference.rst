CLI Reference
=============

This reference documents all available command-line options and commands for ``epub-utils``.

Synopsis
--------

.. code-block:: text

   epub-utils [GLOBAL_OPTIONS] EPUB_FILE COMMAND [COMMAND_OPTIONS]

Global Options
--------------

``-h, --help``
   Show help message and exit

``-v, --version``
   Show program version and exit

``-pp, --pretty-print``
   Pretty-print XML output with proper indentation (applies to xml and raw formats only)

Commands
--------

All commands operate on an EPUB file and support the ``--format`` and ``--pretty-print`` options unless otherwise noted.

container
~~~~~~~~~

Display the container.xml file contents.

**Syntax**:

.. code-block:: bash

   epub-utils EPUB_FILE container [--format FORMAT] [--pretty-print]

**Description**:
The container command shows the contents of META-INF/container.xml, which defines the 
location of the main package file within the EPUB.

**Supported formats**: ``xml`` (default), ``raw``

**Examples**:

.. code-block:: bash

   # Show container with syntax highlighting
   epub-utils book.epub container

   # Show raw container XML
   epub-utils book.epub container --format raw
   
   # Show container with pretty formatting
   epub-utils book.epub container --pretty-print
   
   # Combine both options
   epub-utils book.epub container --format raw --pretty-print
   epub-utils book.epub container --format raw

**Sample output**:

.. code-block:: xml

   <?xml version="1.0" encoding="UTF-8"?>
   <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
     <rootfiles>
       <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
     </rootfiles>
   </container>

package
~~~~~~~

Display the main package (OPF) file contents.

**Syntax**:

.. code-block:: bash

   epub-utils EPUB_FILE package [--format FORMAT] [--pretty-print]

**Description**:
The package command shows the complete OPF (Open Packaging Format) file, which contains 
metadata, manifest, and spine information.

**Supported formats**: ``xml`` (default), ``raw``

**Examples**:

.. code-block:: bash

   # Show package with syntax highlighting
   epub-utils book.epub package

   # Show raw package XML for processing
   epub-utils book.epub package --format raw | xmllint --format -
   
   # Show package with pretty formatting
   epub-utils book.epub package --pretty-print

toc
~~~

Display the table of contents file.

**Syntax**:

.. code-block:: bash

   epub-utils EPUB_FILE toc [--format FORMAT] [--pretty-print] [--ncx | --nav]

**Description**:
Shows the table of contents, which can be either an NCX file (EPUB 2.x) or a 
Navigation Document (EPUB 3.x). By default, automatically detects and uses the 
appropriate format for the EPUB version.

**Options**:

``--ncx``
   Force retrieval of NCX file (EPUB 2 navigation control file). For EPUB 2, 
   this is the same as the default behavior. For EPUB 3, this specifically 
   accesses the NCX file if present for backward compatibility.

``--nav``
   Force retrieval of Navigation Document (EPUB 3 navigation file). Only works 
   with EPUB 3 documents that have a Navigation Document.

**Note**: The ``--ncx`` and ``--nav`` flags are mutually exclusive.

**Supported formats**: ``xml`` (default), ``raw``

**Examples**:

.. code-block:: bash

   # Show TOC with highlighting (auto-detect format)
   epub-utils book.epub toc

   # Extract navigation structure
   epub-utils book.epub toc --format raw
   
   # Show TOC with pretty formatting
   epub-utils book.epub toc --pretty-print

   # Force NCX format (EPUB 2 style)
   epub-utils book.epub toc --ncx

   # Force Navigation Document (EPUB 3 style)
   epub-utils book.epub toc --nav

metadata
~~~~~~~~

Display metadata information from the package file.

**Syntax**:

.. code-block:: bash

   epub-utils EPUB_FILE metadata [--format FORMAT] [--pretty-print]

**Description**:
Extracts and displays Dublin Core and EPUB-specific metadata from the package file.

**Supported formats**: ``xml`` (default), ``raw``, ``kv``

**Examples**:

.. code-block:: bash

   # Show formatted metadata
   epub-utils book.epub metadata

   # Get key-value pairs for scripting
   epub-utils book.epub metadata --format kv

   # Raw metadata XML
   epub-utils book.epub metadata --format raw
   
   # Show metadata with pretty formatting
   epub-utils book.epub metadata --pretty-print

**Key-value output format**:

.. code-block:: text

   title: The Great Gatsby
   creator: F. Scott Fitzgerald
   language: en
   identifier: urn:uuid:12345678-1234-1234-1234-123456789abc
   publisher: Scribner
   date: 2021-01-01
   subject: Fiction, Classic Literature

manifest
~~~~~~~~

Display the manifest section from the package file.

**Syntax**:

.. code-block:: bash

   epub-utils EPUB_FILE manifest [--format FORMAT] [--pretty-print]

**Description**:
Shows the manifest, which lists all files included in the EPUB package with their 
IDs, file paths, and media types.

**Supported formats**: ``xml`` (default), ``raw``

**Examples**:

.. code-block:: bash

   # Show manifest with highlighting
   epub-utils book.epub manifest

   # Find all CSS files
   epub-utils book.epub manifest --format raw | grep 'media-type="text/css"'
   
   # Show manifest with pretty formatting
   epub-utils book.epub manifest --pretty-print
   epub-utils book.epub manifest --format raw | grep 'media-type="text/css"'

   # Count content files
   epub-utils book.epub manifest --format raw | grep -c 'application/xhtml+xml'

spine
~~~~~

Display the spine section from the package file.

**Syntax**:

.. code-block:: bash

   epub-utils EPUB_FILE spine [--format FORMAT] [--pretty-print]

**Description**:
Shows the spine, which defines the default reading order of the book's content.

**Supported formats**: ``xml`` (default), ``raw``

**Examples**:

.. code-block:: bash

   # Show spine with highlighting
   epub-utils book.epub spine

   # Extract reading order
   epub-utils book.epub spine --format raw
   
   # Show spine with pretty formatting
   epub-utils book.epub spine --pretty-print

content
~~~~~~~

Display the content of a document by its manifest item ID.

**Syntax**:

.. code-block:: bash

   epub-utils EPUB_FILE content ITEM_ID [--format FORMAT] [--pretty-print]

**Description**:
Extracts and displays the content of a specific document within the EPUB, identified 
by its manifest item ID.

**Supported formats**: ``xml`` (default), ``raw``, ``plain``

**Arguments**:
- ``ITEM_ID``: The ID of the item as defined in the manifest

**Examples**:

.. code-block:: bash

   # Show content with syntax highlighting
   epub-utils book.epub content chapter1

   # Get raw HTML/XHTML
   epub-utils book.epub content intro --format raw

   # Extract plain text (no HTML tags)
   epub-utils book.epub content chapter2 --format plain
   
   # Show content with pretty formatting
   epub-utils book.epub content chapter1 --pretty-print

**Finding item IDs**:

.. code-block:: bash

   # First check the manifest for available IDs
   epub-utils book.epub manifest | grep 'id='

   # Then extract specific content
   epub-utils book.epub content found_id --format plain

files
~~~~~

List all files in the EPUB archive with metadata, or display content of a specific file.

**Syntax**:

.. code-block:: bash

   epub-utils EPUB_FILE files [FILE_PATH] [--format FORMAT] [--pretty-print]

**Description**:
When used without a file path, provides detailed information about all files contained 
within the EPUB archive, including sizes, compression ratios, and modification dates.

When used with a file path, displays the content of the specified file within the EPUB archive.

**Supported formats**: 

- For file listing: ``table`` (default), ``raw``
- For file content: ``raw``, ``xml`` (default), ``plain``, ``kv``

**Arguments**:
- ``FILE_PATH`` (optional): Path to a specific file within the EPUB archive

**Supported formats**: ``table`` (default), ``raw``

**Examples**:

.. code-block:: bash

   # List all files in table format (default)
   epub-utils book.epub files

   # Get simple file list
   epub-utils book.epub files --format raw

   # Count total files
   epub-utils book.epub files --format raw | wc -l

   # Display content of a specific XHTML file
   epub-utils book.epub files OEBPS/chapter1.xhtml

   # Display XHTML file in different formats
   epub-utils book.epub files OEBPS/chapter1.xhtml --format raw
   epub-utils book.epub files OEBPS/chapter1.xhtml --format xml --pretty-print
   epub-utils book.epub files OEBPS/chapter1.xhtml --format plain

   # Display non-XHTML files (CSS, etc.)
   epub-utils book.epub files OEBPS/styles/main.css

**Key differences from content command**:

- ``files`` uses file paths within the EPUB archive
- ``content`` uses manifest item IDs
- ``files`` can access any file, including CSS, XML, and image files
- ``content`` only accesses files listed in the manifest

**Sample table output**:

.. code-block:: text

   File Information for book.epub
   ┌────────────────────────────────────────┬──────────┬──────────────┬─────────────────────┐
   │ Path                                   │ Size     │ Compressed   │ Modified            │
   ├────────────────────────────────────────┼──────────┼──────────────┼─────────────────────┤
   │ META-INF/container.xml                 │ 230 B    │ 140 B        │ 2021-01-01 10:00:00│
   │ OEBPS/content.opf                      │ 2.1 KB   │ 856 B        │ 2021-01-01 10:00:00│
   │ OEBPS/Text/chapter01.xhtml             │ 12.4 KB  │ 3.2 KB       │ 2021-01-01 10:00:00│
   └────────────────────────────────────────┴──────────┴──────────────┴─────────────────────┘

Format Options
--------------

Most commands support the ``--format`` and ``--pretty-print`` options to control output formatting:

``xml`` (default for most commands)
   Syntax-highlighted, formatted XML output

``raw``
   Unformatted content exactly as stored in the EPUB

``kv`` (metadata command only)
   Key-value pairs suitable for shell scripting

``plain`` (content command only)
   Plain text with HTML tags stripped

``table`` (files command only)
   Formatted table with aligned columns

Pretty Print Option
~~~~~~~~~~~~~~~~~~~

The ``--pretty-print`` (or ``-pp``) option formats XML output with proper indentation and structure:

.. code-block:: bash

   # Default output (with syntax highlighting but compact)
   epub-utils book.epub metadata
   
   # Pretty-printed output (with proper indentation)
   epub-utils book.epub metadata --pretty-print
   
   # Combine with raw format for clean, formatted XML
   epub-utils book.epub package --format raw --pretty-print

**Note**: The pretty-print option applies to both ``xml`` and ``raw`` formats, but has no effect on ``kv``, ``plain``, or ``table`` formats.

Exit Codes
----------

epub-utils uses standard exit codes:

- ``0``: Success
- ``1``: General error (file not found, invalid EPUB, etc.)
- ``2``: Command line usage error

Examples can check exit codes for error handling:

.. code-block:: bash

   if epub-utils book.epub metadata >/dev/null 2>&1; then
       echo "EPUB is valid"
   else
       echo "EPUB has issues"
   fi

Environment Variables
---------------------

epub-utils respects these environment variables:

``NO_COLOR``
   Disable color output when set to any value

``FORCE_COLOR``
   Force color output even when not outputting to a terminal

**Examples**:

.. code-block:: bash

   # Disable colors
   NO_COLOR=1 epub-utils book.epub metadata

   # Force colors in pipes
   FORCE_COLOR=1 epub-utils book.epub metadata | less -R

Common Usage Patterns
---------------------

Validation Workflow
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/zsh
   # validate-epub.sh - Basic EPUB validation

   epub_file="$1"

   echo "Validating: $epub_file"

   # Check container
   if ! epub-utils "$epub_file" container >/dev/null 2>&1; then
       echo "❌ Invalid container"
       exit 1
   fi

   # Check package
   if ! epub-utils "$epub_file" package >/dev/null 2>&1; then
       echo "❌ Invalid package"
       exit 1
   fi

   # Check required metadata
   metadata=$(epub-utils "$epub_file" metadata --format kv 2>/dev/null)
   if ! echo "$metadata" | grep -q "^title:"; then
       echo "⚠️  Missing title"
   fi

   if ! echo "$metadata" | grep -q "^creator:"; then
       echo "⚠️  Missing author"
   fi

   echo "✅ EPUB structure is valid"

Metadata Extraction
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/zsh
   # extract-metadata.sh - Extract metadata to CSV

   echo "filename,title,author,language,publisher" > metadata.csv

   for epub in *.epub; do
       if [[ -f "$epub" ]]; then
           metadata=$(epub-utils "$epub" metadata --format kv 2>/dev/null)
           
           title=$(echo "$metadata" | grep "^title:" | cut -d' ' -f2- | tr ',' ';')
           author=$(echo "$metadata" | grep "^creator:" | cut -d' ' -f2- | tr ',' ';')
           language=$(echo "$metadata" | grep "^language:" | cut -d' ' -f2-)
           publisher=$(echo "$metadata" | grep "^publisher:" | cut -d' ' -f2- | tr ',' ';')
           
           echo "$epub,$title,$author,$language,$publisher" >> metadata.csv
       fi
   done

Content Analysis
~~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/zsh
   # analyze-content.sh - Analyze EPUB content structure

   epub_file="$1"

   echo "Content Analysis for: $epub_file"
   echo "=================================="

   # Get content files from manifest
   content_ids=$(epub-utils "$epub_file" manifest --format raw | \
                grep 'media-type="application/xhtml+xml"' | \
                sed 's/.*id="\([^"]*\)".*/\1/')

   total_words=0

   for content_id in $content_ids; do
       if word_count=$(epub-utils "$epub_file" content "$content_id" --format plain 2>/dev/null | wc -w); then
           echo "Content ID '$content_id': $word_count words"
           total_words=$((total_words + word_count))
       fi
   done

   echo "=================================="
   echo "Total words: $total_words"

Error Handling
--------------

Always handle errors when using epub-utils in scripts:

.. code-block:: bash

   # Check if file exists first
   if [[ ! -f "$epub_file" ]]; then
       echo "Error: File '$epub_file' not found" >&2
       exit 1
   fi

   # Capture and handle command errors
   if ! output=$(epub-utils "$epub_file" metadata --format kv 2>&1); then
       echo "Error processing EPUB: $output" >&2
       exit 1
   fi

   # Check for specific issues
   if [[ -z "$output" ]]; then
       echo "Warning: No metadata found" >&2
   fi

Performance Tips
----------------

1. **Use raw format for large-scale processing** to avoid syntax highlighting overhead
2. **Pipe efficiently** to avoid unnecessary intermediate files
3. **Process files in parallel** when handling many EPUBs
4. **Cache results** when running the same command multiple times

.. code-block:: bash

   # Efficient parallel processing
   find . -name "*.epub" | xargs -n 1 -P 4 -I {} \
       zsh -c 'echo "{}: $(epub-utils "{}" metadata --format kv | grep "^title:" | cut -d" " -f2-)"'

Troubleshooting
---------------

Common Issues and Solutions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**"Invalid value for 'PATH': File does not exist"**
   Check the file path and ensure the EPUB file exists.

**"ParseError: Unable to parse container.xml"**
   The EPUB file may be corrupted. Verify it's a valid ZIP file.

**"Content with id 'X' not found"**
   Check available content IDs using the manifest command first.

**No color output**
   Ensure your terminal supports colors and check the ``NO_COLOR`` environment variable.

**Large file performance**
   Use ``--format raw`` for better performance with large files.
