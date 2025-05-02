# epub-utils

[![PyPI](https://img.shields.io/pypi/v/epub-utils.svg)](https://pypi.org/project/epub-utils/)
[![Python 3.x](https://img.shields.io/pypi/pyversions/epub-utils.svg?logo=python&logoColor=white)](https://pypi.org/project/epub-utils/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/ernestofgonzalez/epub-utils/blob/main/LICENSE)

A Python CLI and utility library for manipulating EPUB files.

## Features

- Parse and validate EPUB container and package files
- Extract metadata like title, author, and identifier
- Command-line interface for quick file inspection
- Syntax highlighted XML output

## Quick Start

1. Install the package:
```bash
pip install epub-utils
```

2. Use as a CLI tool:
```bash
# Show container.xml contents
epub-utils your-book.epub container

# Show package OPF contents
epub-utils your-book.epub package

# Show table of contents
epub-utils your-book.epub toc
```

3. Use as a Python library:
```python
from epub_utils import Document

# Load an EPUB document
doc = Document("path/to/book.epub")

# Access container metadata
print(f"Package file location: {doc.container.rootfile_path}")

# Access package metadata
print(f"Title: {doc.package.title}")
print(f"Author: {doc.package.author}")
print(f"Identifier: {doc.package.identifier}")
```