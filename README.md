# epub-utils

[![PyPI](https://img.shields.io/pypi/v/epub-utils.svg)](https://pypi.org/project/epub-utils/)
[![Changelog](https://img.shields.io/github/v/release/ernestofgonzalez/epub-utils?include_prereleases&label=changelog)](https://ernestofgonzalez.github.io/epub-utils/changelog)
[![Python 3.x](https://img.shields.io/pypi/pyversions/epub-utils.svg?logo=python&logoColor=white)](https://pypi.org/project/epub-utils/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/ernestofgonzalez/epub-utils/blob/main/LICENSE)

A Python library and CLI tool for inspecting ePub from the terminal.

## Features

- **Complete EPUB Support** - Parse both EPUB 2.0.1 and EPUB 3.0+ specifications with container, package, manifest, spine, and table of contents inspection
- **Rich Metadata Extraction** - Extract Dublin Core metadata (title, author, language, publisher) with key-value, XML, and raw output formats for easy scripting
- **Content Analysis** - Access document content by manifest ID or file path, with plain text extraction for content analysis and word counting
- **File System Navigation** - Browse and extract any file within EPUB archives (XHTML, CSS, images, fonts) with detailed file information including sizes and compression ratios
- **Multiple Output Formats** - XML with syntax highlighting, raw content, key-value pairs, plain text, and formatted tables to suit different workflows
- **CLI and Python API** - Comprehensive command-line tool for terminal workflows plus a clean Python library for programmatic access
- **Standards Compliance** - Built-in validation capabilities and adherence to W3C/IDPF specifications for reliable EPUB processing
- **Performance Optimized** - Lazy loading, efficient ZIP parsing, and optional lxml support for handling large EPUB collections

## Installation

`epub-utils` is available as a [PyPI](https://pypi.org/) package

```bash
pip install epub-utils
```

## Use as a CLI tool

The basic format is:

```bash
epub-utils EPUB_PATH COMMAND [OPTIONS]
```

### Commands

- `container` - Display the container.xml contents
    ```bash
    # Show container.xml with syntax highlighting
    epub-utils book.epub container

    # Show container.xml as raw content
    epub-utils book.epub container --format raw
    
    # Show container.xml with pretty formatting
    epub-utils book.epub container --pretty-print
    ```

- `package` - Display the package OPF file contents
    ```bash
    # Show package.opf with syntax highlighting
    epub-utils book.epub package

    # Show package.opf as raw content
    epub-utils book.epub package --format raw
    ```

- `toc` - Display the table of contents file contents
    ```bash
    # Show toc.ncx/nav.xhtml with syntax highlighting
    epub-utils book.epub toc

    # Show toc.ncx/nav.xhtml as raw content
    epub-utils book.epub toc --format raw
    ```

- `metadata` - Display the metadata information from the package file
    ```bash
    # Show metadata with syntax highlighting
    epub-utils book.epub metadata

    # Show metadata as key-value pairs
    epub-utils book.epub metadata --format kv
    
    # Show metadata with pretty formatting
    epub-utils book.epub metadata --pretty-print
    ```

- `manifest` - Display the manifest information from the package file
    ```bash
    # Show manifest with syntax highlighting
    epub-utils book.epub manifest

    # Show manifest as raw content
    epub-utils book.epub manifest --format raw
    ```

- `spine` - Display the spine information from the package file
    ```bash
    # Show spine with syntax highlighting
    epub-utils book.epub spine

    # Show spine as raw content
    epub-utils book.epub spine --format raw
    ```

- `content` - Display the content of a document by its manifest item ID
    ```bash
    # Show content with syntax highlighting
    epub-utils book.epub content chapter1

    # Show raw HTML/XML content
    epub-utils book.epub content chapter1 --format raw
    
    # Show plain text content (HTML tags stripped)
    epub-utils book.epub content chapter1 --format plain
    ```

- `files` - List all files in the EPUB archive or display content of a specific file
    ```bash
    # List all files in table format (default)
    epub-utils book.epub files

    # List all files as simple paths
    epub-utils book.epub files --format raw

    # Display content of a specific file by path
    epub-utils book.epub files OEBPS/chapter1.xhtml

    # Display XHTML file content in different formats
    epub-utils book.epub files OEBPS/chapter1.xhtml --format raw
    epub-utils book.epub files OEBPS/chapter1.xhtml --format xml --pretty-print
    epub-utils book.epub files OEBPS/chapter1.xhtml --format plain

    # Display non-XHTML files (CSS, images, etc.)
    epub-utils book.epub files OEBPS/styles/main.css
    epub-utils book.epub files META-INF/container.xml
    ```

### Options

- `-h, --help` - Show help message and exit
- `-v, --version` - Show program version and exit
- `-fmt, --format` - Output format (default: xml)
    - `xml` - Display with XML syntax highlighting (default)
    - `raw` - Display raw content without formatting
    - `plain` - Display plain text content (HTML tags stripped, for content command only)
    - `kv` - Display key-value pairs (where supported)
- `-pp, --pretty-print` - Pretty-print XML output (applies to xml and raw formats only)
    
    ```bash
    # Display as raw content
    epub-utils book.epub package --format raw
    
    # Display with XML syntax highlighting (default)
    epub-utils book.epub package --format xml
    
    # Display as key-value pairs (for supported commands)
    epub-utils book.epub metadata --format kv
    
    # Display plain text content (content command only)
    epub-utils book.epub content chapter1 --format plain
    
    # Pretty-print XML with proper indentation
    epub-utils book.epub package --pretty-print
    
    # Combine format and pretty-print options
    epub-utils book.epub metadata --format raw --pretty-print
    ```

## Use as a Python library

```python
from epub_utils import Document

# Load an EPUB document
doc = Document("path/to/book.epub")
```

### Basic Document Access

Access the main components of an EPUB document:

```python
# Get container information
container = doc.container
print(container.to_xml())  # Formatted XML with syntax highlighting
print(container.to_str())  # Raw XML content

# Get package information  
package = doc.package
print(package.to_xml())    # Formatted XML with syntax highlighting
print(package.to_str())    # Raw XML content

# Get table of contents
toc = doc.toc
if toc:  # TOC might be None if not present
    print(toc.to_xml())    # Formatted XML with syntax highlighting
    print(toc.to_str())    # Raw XML content
```

### Working with Metadata

Access and format metadata information:

```python
# Access package metadata
metadata = doc.package.metadata

# Basic Dublin Core elements
print(f"Title: {metadata.title}")
print(f"Creator: {metadata.creator}")
print(f"Identifier: {metadata.identifier}")
print(f"Language: {metadata.language}")
print(f"Publisher: {metadata.publisher}")
print(f"Date: {metadata.date}")

# Dynamic attribute access for any metadata field
isbn = getattr(metadata, 'isbn', 'Not available')
series = getattr(metadata, 'series', 'Not available')

# Get formatted metadata output
print(metadata.to_xml())     # Formatted XML with syntax highlighting
print(metadata.to_str())     # Raw XML content  
print(metadata.to_kv())      # Key-value format for easy parsing
```

### Working with Manifest

Access the manifest to see all files in the EPUB:

```python
# Get manifest information
manifest = doc.package.manifest

# Access all manifest items
for item in manifest.items:
    print(f"ID: {item['id']}")
    print(f"File: {item['href']}")
    print(f"Type: {item['media_type']}")
    print(f"Properties: {item['properties']}")

# Find specific items
nav_item = manifest.find_by_property('nav')
chapter = manifest.find_by_id('chapter1')
xhtml_items = manifest.find_by_media_type('application/xhtml+xml')

# Get formatted manifest output
print(manifest.to_xml())     # Formatted XML with syntax highlighting
print(manifest.to_str())     # Raw XML content
```

### Working with Spine

Access the spine to see the reading order:

```python
# Get spine information
spine = doc.package.spine

# Access spine properties
print(f"TOC reference: {spine.toc}")
print(f"Page progression: {spine.page_progression_direction}")

# Access spine items in reading order
for itemref in spine.itemrefs:
    print(f"ID: {itemref['idref']}")
    print(f"Linear: {itemref['linear']}")
    print(f"Properties: {itemref['properties']}")

# Find specific spine item
spine_item = spine.find_by_idref('chapter1')

# Get formatted spine output
print(spine.to_xml())        # Formatted XML with syntax highlighting
print(spine.to_str())        # Raw XML content
```

### Content Extraction

Extract content from specific documents within the EPUB:

```python
# Access content by manifest item ID
try:
    content = doc.find_content_by_id('chapter1')
    
    # Get content in different formats
    print(content.to_xml())      # Formatted XHTML with syntax highlighting
    print(content.to_str())      # Raw XHTML content
    print(content.to_plain())    # Plain text with HTML tags stripped
    
    # Access the parsed content tree for advanced processing
    tree = content.tree
    inner_text = content.inner_text
    
except ValueError as e:
    print(f"Content not found: {e}")

# Find publication resources by ID (for non-spine items)
try:
    resource = doc.find_pub_resource_by_id('cover-image')
except ValueError as e:
    print(f"Resource not found: {e}")
```

### File Operations

List and access files directly by their paths in the EPUB archive:

```python
# Get information about all files
files_info = doc.get_files_info()
for file_info in files_info:
    print(f"Path: {file_info['path']}")
    print(f"Size: {file_info['size']} bytes")
    print(f"Compressed: {file_info['compressed_size']} bytes")
    print(f"Modified: {file_info['modified']}")

# Access specific file by path
try:
    # For XHTML files, returns XHTMLContent object
    xhtml_content = doc.get_file_by_path('OEBPS/chapter1.xhtml')
    print(xhtml_content.to_xml())
    print(xhtml_content.to_plain())
    
    # For other files, returns raw string content
    css_content = doc.get_file_by_path('OEBPS/styles/main.css')
    print(css_content)
    
except ValueError as e:
    print(f"File not found: {e}")
```

### Output Formatting Options

All document components support flexible output formatting:

```python
# Pretty-printed XML output
print(metadata.to_str(pretty_print=True))
print(manifest.to_xml(pretty_print=True))

# Syntax highlighting can be controlled
print(package.to_xml(highlight_syntax=True))   # With highlighting (default)
print(package.to_xml(highlight_syntax=False))  # Without highlighting
```

## Industry Standards & Compliance

`epub-utils` provides comprehensive support for industry-standard ePub specifications and related technologies, ensuring broad compatibility across the digital publishing ecosystem.

### Supported EPUB Standards

- **EPUB 2.0.1** (IDPF, 2010)
  - Complete OPF 2.0 package document support
  - NCX navigation control file support
  - Dublin Core metadata extraction
  - Legacy EPUB compatibility

- **EPUB 3.0+** (IDPF/W3C, 2011-present)
  - EPUB 3.3 specification compliance
  - HTML5-based content documents
  - Navigation document (nav.xhtml) support
  - Enhanced accessibility features
  - Media overlays and scripting support

### Metadata Standards

- **Dublin Core Metadata Initiative (DCMI)**
  - Dublin Core Metadata Element Set v1.1
  - Dublin Core Metadata Terms (DCTERMS)

- **Open Packaging Format (OPF)**
  - OPF 2.0 specification (EPUB 2.0.1)
  - OPF 3.0 specification (EPUB 3.0+)

The library maintains strict adherence to published specifications while providing robust handling of real-world EPUB variations commonly found in commercial and open-source reading applications.