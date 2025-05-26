Output Formats Reference
========================

``epub-utils`` supports multiple output formats to suit different use cases. This guide explains each 
format with examples and best practices for when to use each one.

Overview
--------

All commands in ``epub-utils`` support the ``--format`` option with these values:

- ``xml`` - Syntax-highlighted XML (default for most commands)
- ``raw`` - Unformatted, raw content
- ``kv`` - Key-value pairs (where supported)
- ``plain`` - Plain text with HTML tags stripped (content command only)
- ``table`` - Formatted table (files command only)

XML Format (Default)
--------------------

The XML format provides syntax-highlighted, pretty-printed XML output that's easy to read.

**When to use**: Interactive inspection, debugging, learning EPUB structure

**Example**:

.. code-block:: bash

   $ epub-utils book.epub metadata --format xml

**Output**:

.. code-block:: xml

   <?xml version="1.0" encoding="UTF-8"?>
   <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" 
             xmlns:opf="http://www.idpf.org/2007/opf">
     <dc:title>The Great Gatsby</dc:title>
     <dc:creator>F. Scott Fitzgerald</dc:creator>
     <dc:language>en</dc:language>
     <dc:identifier id="bookid">urn:uuid:12345678-1234-1234-1234-123456789abc</dc:identifier>
     <dc:publisher>Scribner</dc:publisher>
     <dc:date>2021-01-01</dc:date>
     <dc:subject>Fiction</dc:subject>
     <dc:subject>Classic Literature</dc:subject>
   </metadata>

**Features**:
- Color syntax highlighting
- Proper indentation
- Easy to read structure
- Preserves all XML attributes and namespaces

Raw Format
----------

The raw format outputs unprocessed content exactly as stored in the EPUB file.

**When to use**: Piping to other tools, automated processing, debugging XML issues

**Example**:

.. code-block:: bash

   $ epub-utils book.epub metadata --format raw

**Output**:

.. code-block:: xml

   <?xml version="1.0" encoding="UTF-8"?><metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf"><dc:title>The Great Gatsby</dc:title><dc:creator>F. Scott Fitzgerald</dc:creator><dc:language>en</dc:language><dc:identifier id="bookid">urn:uuid:12345678-1234-1234-1234-123456789abc</dc:identifier><dc:publisher>Scribner</dc:publisher><dc:date>2021-01-01</dc:date><dc:subject>Fiction</dc:subject><dc:subject>Classic Literature</dc:subject></metadata>

**Use cases**:

.. code-block:: bash

   # Pipe to xmllint for custom formatting
   $ epub-utils book.epub package --format raw | xmllint --format -

   # Extract specific elements with grep
   $ epub-utils book.epub manifest --format raw | grep 'media-type="text/css"'

   # Validate XML structure
   $ epub-utils book.epub toc --format raw | xmllint --valid -

Key-Value Format
----------------

The key-value format presents metadata as simple ``key: value`` pairs, perfect for scripting.

**When to use**: Shell scripting, automated data extraction, configuration files

**Supported commands**: ``metadata``

**Example**:

.. code-block:: bash

   $ epub-utils book.epub metadata --format kv

**Output**:

.. code-block:: text

   title: The Great Gatsby
   creator: F. Scott Fitzgerald
   language: en
   identifier: urn:uuid:12345678-1234-1234-1234-123456789abc
   publisher: Scribner
   date: 2021-01-01
   subject: Fiction, Classic Literature

**Scripting examples**:

.. code-block:: bash

   # Extract just the title
   title=$(epub-utils book.epub metadata --format kv | grep "^title:" | cut -d' ' -f2-)

   # Get all metadata into shell variables
   eval "$(epub-utils book.epub metadata --format kv | sed 's/^/meta_/')"
   echo "Book title: $meta_title"
   echo "Author: $meta_creator"

   # Create a simple database
   echo "filename,title,author" > books.csv
   for epub in *.epub; do
       metadata=$(epub-utils "$epub" metadata --format kv)
       title=$(echo "$metadata" | grep "^title:" | cut -d' ' -f2- | tr ',' ';')
       author=$(echo "$metadata" | grep "^creator:" | cut -d' ' -f2- | tr ',' ';')
       echo "$epub,$title,$author" >> books.csv
   done

Plain Text Format
-----------------

The plain text format strips HTML tags and returns readable text content.

**When to use**: Content analysis, word counting, text extraction

**Supported commands**: ``content``

**Example**:

.. code-block:: bash

   $ epub-utils book.epub content chapter1 --format plain

**Output**:

.. code-block:: text

   Chapter 1: The Beginning

   In my younger and more vulnerable years my father gave me some advice 
   that I've carried with me ever since. "Whenever you feel like criticizing 
   anyone," he told me, "just remember that all the people in this world 
   haven't had the advantages that you've had."

**Use cases**:

.. code-block:: bash

   # Count words in a chapter
   word_count=$(epub-utils book.epub content chapter1 --format plain | wc -w)
   echo "Chapter 1 has $word_count words"

   # Extract all text for analysis
   epub-utils book.epub content intro --format plain > intro.txt

   # Search for specific content
   if epub-utils book.epub content chapter2 --format plain | grep -q "important phrase"; then
       echo "Found the phrase in chapter 2"
   fi

Table Format
------------

The table format presents file information in a readable tabular layout.

**When to use**: File analysis, human-readable file listings

**Supported commands**: ``files``

**Example**:

.. code-block:: bash

   $ epub-utils book.epub files --format table

**Output**:

.. code-block:: text

   File Information for book.epub
   ┌────────────────────────────────────────┬──────────┬──────────────┬─────────────────────┐
   │ Path                                   │ Size     │ Compressed   │ Modified            │
   ├────────────────────────────────────────┼──────────┼──────────────┼─────────────────────┤
   │ META-INF/container.xml                 │ 230 B    │ 140 B        │ 2021-01-01 10:00:00│
   │ OEBPS/content.opf                      │ 2.1 KB   │ 856 B        │ 2021-01-01 10:00:00│
   │ OEBPS/toc.ncx                          │ 1.8 KB   │ 542 B        │ 2021-01-01 10:00:00│
   │ OEBPS/Text/chapter01.xhtml             │ 12.4 KB  │ 3.2 KB       │ 2021-01-01 10:00:00│
   │ OEBPS/Text/chapter02.xhtml             │ 15.6 KB  │ 4.1 KB       │ 2021-01-01 10:00:00│
   │ OEBPS/Styles/stylesheet.css            │ 3.2 KB   │ 1.1 KB       │ 2021-01-01 10:00:00│
   │ OEBPS/Images/cover.jpg                 │ 145.2 KB │ 144.8 KB     │ 2021-01-01 10:00:00│
   └────────────────────────────────────────┴──────────┴──────────────┴─────────────────────┘

Command-Specific Format Support
-------------------------------

Here's a quick reference for which formats each command supports:

.. list-table:: Format Support by Command
   :header-rows: 1
   :widths: 20 15 15 15 15 15

   * - Command
     - XML
     - Raw
     - KV
     - Plain
     - Table
   * - ``container``
     - ✓
     - ✓
     - ✗
     - ✗
     - ✗
   * - ``package``
     - ✓
     - ✓
     - ✗
     - ✗
     - ✗
   * - ``toc``
     - ✓
     - ✓
     - ✗
     - ✗
     - ✗
   * - ``metadata``
     - ✓
     - ✓
     - ✓
     - ✗
     - ✗
   * - ``manifest``
     - ✓
     - ✓
     - ✗
     - ✗
     - ✗
   * - ``spine``
     - ✓
     - ✓
     - ✗
     - ✗
     - ✗
   * - ``content``
     - ✓
     - ✓
     - ✗
     - ✓
     - ✗
   * - ``files``
     - ✗
     - ✓
     - ✗
     - ✗
     - ✓

Advanced Format Usage
---------------------

Combining Formats with Shell Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Pretty-print with custom tools**:

.. code-block:: bash

   # Use xmllint for custom XML formatting
   epub-utils book.epub package --format raw | xmllint --format --noblanks -

   # Convert to JSON using xq (if available)
   epub-utils book.epub metadata --format raw | xq '.'

**Processing key-value output**:

.. code-block:: bash

   # Convert to environment variables
   export $(epub-utils book.epub metadata --format kv | tr ' ' '_' | tr ':' '=')
   echo "Title: $title"

   # Create YAML-like output
   epub-utils book.epub metadata --format kv | sed 's/^/  /' | sed '1i metadata:'

**Text analysis workflows**:

.. code-block:: bash

   # Analyze reading time (assuming 200 words per minute)
   words=$(epub-utils book.epub content chapter1 --format plain | wc -w)
   minutes=$((words / 200))
   echo "Chapter 1 reading time: $minutes minutes"

   # Extract quotes (lines starting with quotation marks)
   epub-utils book.epub content chapter1 --format plain | grep '^".*"$'

Format Selection Guidelines
---------------------------

Choose the right format based on your use case:

**For Human Reading**:
- Use ``xml`` for inspecting EPUB structure
- Use ``table`` for file listings
- Use ``plain`` for content reading

**For Automation**:
- Use ``raw`` for piping to other XML tools
- Use ``kv`` for simple scripting and data extraction
- Use ``raw`` with ``files`` for getting simple file lists

**For Integration**:
- Use ``raw`` when feeding into other programs
- Use ``kv`` for configuration file generation
- Use ``plain`` for text processing workflows

**Performance Considerations**:
- ``raw`` format is fastest (no syntax highlighting)
- ``xml`` format has slight overhead for highlighting
- ``table`` format requires additional formatting computation

Error Handling with Formats
----------------------------

Different formats handle errors differently:

.. code-block:: bash

   # XML format shows formatted error messages
   $ epub-utils corrupted.epub metadata --format xml
   Error: Unable to parse metadata

   # Raw format may show parsing errors directly
   $ epub-utils corrupted.epub metadata --format raw
   ParseError: Invalid XML structure

   # KV format gracefully handles missing fields
   $ epub-utils incomplete.epub metadata --format kv
   title: 
   creator: Unknown Author
   language: en

Custom Format Processing
------------------------

You can create custom output formats by post-processing the raw output:

.. code-block:: bash

   #!/bin/zsh
   # custom-json-format.sh - Convert metadata to JSON

   epub_file="$1"

   echo "{"
   epub-utils "$epub_file" metadata --format kv | while IFS=': ' read -r key value; do
       if [[ -n "$key" && -n "$value" ]]; then
           echo "  \"$key\": \"$value\","
       fi
   done | sed '$s/,$//'
   echo "}"

.. code-block:: bash

   #!/bin/zsh
   # custom-markdown-format.sh - Convert metadata to Markdown

   epub_file="$1"
   
   echo "# Book Information"
   echo ""
   
   epub-utils "$epub_file" metadata --format kv | while IFS=': ' read -r key value; do
       if [[ -n "$key" && -n "$value" ]]; then
           formatted_key=$(echo "$key" | sed 's/\b\w/\U&/g')  # Title case
           echo "**$formatted_key**: $value"
       fi
   done

Best Practices
--------------

1. **Default to XML for interactive use** - it's the most readable
2. **Use raw for scripting** - it's the most reliable for automation
3. **Use kv for metadata extraction** - it's purpose-built for simple parsing
4. **Use plain for content analysis** - it removes HTML complexity
5. **Always handle errors** - EPUB files can be malformed
6. **Test with various EPUB files** - format output can vary with different EPUB structures

These format options make epub-utils flexible enough to handle everything from quick 
interactive inspection to complex automated workflows.
