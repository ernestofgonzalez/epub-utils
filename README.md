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

    # Show container.xml as plain text
    epub-utils book.epub container --format text
    ```

- `package` - Display the package OPF file contents
    ```bash
    # Show package.opf with syntax highlighting
    epub-utils book.epub package

    # Show package.opf as plain text
    epub-utils book.epub package --format text
    ```

- `toc` - Display the table of contents file contents
    ```bash
    # Show toc.ncx/nav.xhtml with syntax highlighting
    epub-utils book.epub toc

    # Show toc.ncx/nav.xhtml as plain text
    epub-utils book.epub toc --format text
    ```

### Options

- `-h, --help` - Show help message and exit
- `-v, --version` - Show program version and exit
- `-fmt, --format` - Output format, either 'text' or 'xml' (default: xml)
    ```bash
    # Display as plain text
    epub-utils book.epub package --format text
    
    # Display with XML syntax highlighting (default)
    epub-utils book.epub package --format xml
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