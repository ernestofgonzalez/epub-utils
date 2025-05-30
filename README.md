# epub-utils

[![PyPI](https://img.shields.io/pypi/v/epub-utils.svg)](https://pypi.org/project/epub-utils/)
[![Changelog](https://img.shields.io/github/v/release/ernestofgonzalez/epub-utils?include_prereleases&label=changelog)](https://ernestofgonzalez.github.io/epub-utils/changelog)
[![Python 3.x](https://img.shields.io/pypi/pyversions/epub-utils.svg?logo=python&logoColor=white)](https://pypi.org/project/epub-utils/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/ernestofgonzalez/epub-utils/blob/main/LICENSE)

A Python library and CLI tool for inspecting ePub from the terminal.

## Features

- Parse and validate EPUB container and package files
- Extract metadata like title, author, and identifier
- Command-line interface for quick file inspection
- Syntax highlighted XML output

## Installation

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

# Get raw XML content
print(doc.container)
print(doc.package)
print(doc.toc)

# Access package metadata
print(f"Title: {doc.package.metadata.title}")
print(f"Creator: {doc.package.metadata.creator}")
print(f"Identifier: {doc.package.metadata.identifier}")
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