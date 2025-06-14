==============
EPUB Standards
==============

Understanding EPUB Specifications
=================================

EPUB (Electronic Publication) is an open standard for digital books and publications. 
This guide covers the EPUB specifications and how epub-utils ensures compliance.

EPUB 3.3 Specification
======================

Current Standard
----------------

EPUB 3.3 is the current specification, published by the W3C. It defines:

- **Package Document**: Contains metadata, manifest, and spine
- **Container Format**: ZIP-based archive structure
- **Content Documents**: XHTML5, SVG, and other media types
- **Navigation Document**: Replaces NCX for table of contents

Key Components
--------------

Container Structure
~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    book.epub
    ├── META-INF/
    │   ├── container.xml          # Points to package document
    │   └── signatures.xml         # Digital signatures (optional)
    ├── OEBPS/                     # Content folder (common name)
    │   ├── package.opf            # Package document
    │   ├── nav.xhtml              # Navigation document
    │   ├── content/               # Text content
    │   ├── images/                # Images
    │   ├── styles/                # CSS files
    │   └── fonts/                 # Font files (optional)
    └── mimetype                   # Must be first file, uncompressed

Package Document (OPF)
~~~~~~~~~~~~~~~~~~~~~~

The package document defines three main sections:

**Metadata Section**:

.. code-block:: xml

    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:title>Book Title</dc:title>
        <dc:creator>Author Name</dc:creator>
        <dc:identifier id="bookid">urn:uuid:12345</dc:identifier>
        <dc:language>en</dc:language>
        <meta property="dcterms:modified">2024-01-01T00:00:00Z</meta>
    </metadata>

**Manifest Section**:

.. code-block:: xml

    <manifest>
        <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" 
              properties="nav"/>
        <item id="chapter1" href="content/chapter1.xhtml" 
              media-type="application/xhtml+xml"/>
        <item id="cover-image" href="images/cover.jpg" 
              media-type="image/jpeg" properties="cover-image"/>
    </manifest>

**Spine Section**:

.. code-block:: xml

    <spine>
        <itemref idref="chapter1"/>
        <itemref idref="chapter2"/>
    </spine>

Navigation Document
~~~~~~~~~~~~~~~~~~~

EPUB 3 uses XHTML navigation documents instead of NCX:

.. code-block:: html

    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml" 
          xmlns:epub="http://www.idpf.org/2007/ops">
    <head>
        <title>Navigation</title>
    </head>
    <body>
        <nav epub:type="toc">
            <h1>Table of Contents</h1>
            <ol>
                <li><a href="content/chapter1.xhtml">Chapter 1</a></li>
                <li><a href="content/chapter2.xhtml">Chapter 2</a></li>
            </ol>
        </nav>
    </body>
    </html>

EPUB Compliance with epub-utils
===============================

Validation Capabilities
-----------------------

epub-utils helps ensure EPUB compliance by:

1. **Structure Validation**: Checks container format
2. **Metadata Validation**: Verifies required elements
3. **Manifest Validation**: Ensures all files are declared
4. **Spine Validation**: Checks reading order
5. **Content Validation**: Basic XHTML structure checks

Checking Compliance
-------------------

Use epub-utils to validate EPUB structure:

.. code-block:: bash

    # Check basic structure
    epub-utils info book.epub

    # Detailed manifest information
    epub-utils manifest book.epub --format table

    # Extract and examine package document
    epub-utils extract book.epub --output-dir temp/
    cat temp/OEBPS/package.opf

Python API for Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from epub_utils import Document

    def validate_epub_structure(epub_path):
        """Validate basic EPUB structure."""
        try:
            doc = Document(epub_path)
            
            # Check required components
            checks = {
                'has_container': hasattr(doc, 'container'),
                'has_package': hasattr(doc, 'package'),
                'has_metadata': len(doc.metadata) > 0,
                'has_manifest': len(doc.manifest) > 0,
                'has_spine': len(doc.spine) > 0,
            }
            
            # Check required metadata
            required_metadata = ['title', 'language', 'identifier']
            metadata_present = {}
            
            for item in doc.metadata:
                for req in required_metadata:
                    if req in item.get('name', '').lower():
                        metadata_present[req] = True
            
            print("Structure Validation:")
            for check, passed in checks.items():
                status = "✓" if passed else "✗"
                print(f"  {status} {check}")
            
            print("\nRequired Metadata:")
            for req in required_metadata:
                status = "✓" if metadata_present.get(req) else "✗"
                print(f"  {status} {req}")
                
            return all(checks.values()) and len(metadata_present) >= 2
            
        except Exception as e:
            print(f"Validation failed: {e}")
            return False

Common Compliance Issues
========================

Missing Required Elements
-------------------------

**Problem**: EPUB missing required metadata

.. code-block:: bash

    # Check metadata completeness
    epub-utils metadata book.epub --format table

**Solution**: Ensure these elements are present:

- ``dc:title``
- ``dc:language`` 
- ``dc:identifier`` (with unique ID)
- ``meta property="dcterms:modified"`` (EPUB 3)

Invalid File References
-----------------------

**Problem**: Manifest references files that don't exist

.. code-block:: python

    def check_file_references(epub_path):
        """Check if all manifest files exist in the archive."""
        doc = Document(epub_path)
        
        missing_files = []
        for item in doc.manifest:
            file_path = item.get('href')
            if file_path:
                # Check if file exists in the EPUB
                try:
                    # This would need zip file checking
                    pass  
                except:
                    missing_files.append(file_path)
        
        if missing_files:
            print("Missing files referenced in manifest:")
            for file in missing_files:
                print(f"  - {file}")

Incorrect MIME Types
--------------------

**Problem**: Wrong media-type attributes in manifest

Common correct MIME types:

- XHTML: ``application/xhtml+xml``
- CSS: ``text/css``
- JPEG: ``image/jpeg``
- PNG: ``image/png``
- NCX: ``application/x-dtbncx+xml``

EPUB 2 vs EPUB 3 Differences
============================

Format Evolution
-----------------

+------------------+-------------------------+-------------------------+
| Feature          | EPUB 2                  | EPUB 3                  |
+==================+=========================+=========================+
| Navigation       | NCX file required       | XHTML nav document      |
+------------------+-------------------------+-------------------------+
| Content Types    | XHTML 1.1, limited      | XHTML5, SVG, MathML     |
+------------------+-------------------------+-------------------------+
| Metadata         | Dublin Core only        | Enhanced metadata       |
+------------------+-------------------------+-------------------------+
| Accessibility    | Limited                 | Rich accessibility      |
+------------------+-------------------------+-------------------------+
| Scripting        | Not allowed             | Limited JavaScript      |
+------------------+-------------------------+-------------------------+

Migration Considerations
------------------------

When working with older EPUB 2 files:

.. code-block:: python

    def detect_epub_version(epub_path):
        """Detect EPUB version from package document."""
        doc = Document(epub_path)
        
        # Check package document for version attribute
        # This is a simplified example
        for item in doc.manifest:
            if 'nav' in item.get('properties', ''):
                return "EPUB 3"
        
        # Check for NCX file (EPUB 2 indicator)
        for item in doc.manifest:
            if item.get('media-type') == 'application/x-dtbncx+xml':
                return "EPUB 2"
        
        return "Unknown"

Best Practices for Compliance
=============================

Metadata Best Practices
-----------------------

1. **Always include required elements**:

   .. code-block:: xml

       <dc:title>Complete Book Title</dc:title>
       <dc:creator>Author Full Name</dc:creator>
       <dc:identifier id="bookid">urn:uuid:unique-identifier</dc:identifier>
       <dc:language>en-US</dc:language>

2. **Use proper Dublin Core refinements**:

   .. code-block:: xml

       <dc:creator id="author">Jane Doe</dc:creator>
       <meta refines="#author" property="role" scheme="marc:relators">aut</meta>

3. **Include modification date for EPUB 3**:

   .. code-block:: xml

       <meta property="dcterms:modified">2024-05-25T10:30:00Z</meta>

File Organization
-----------------

1. **Use consistent folder structure**
2. **Declare all files in manifest**
3. **Use proper MIME types**
4. **Include fallbacks for specialized content**

Content Guidelines
------------------

1. **Valid XHTML**: Ensure all content files are well-formed
2. **Proper encoding**: Use UTF-8 encoding
3. **Relative links**: Use relative paths for internal references
4. **Alt text**: Include alt attributes for images

Testing and Validation Tools
============================

External Validators
-------------------

- **EPUBCheck**: Official EPUB validator
- **Ace by DAISY**: Accessibility checker
- **pagina EPUB-Checker**: Online validator

Integration with epub-utils
---------------------------

.. code-block:: bash

    # Basic structure check
    epub-utils info book.epub

    # Export for external validation
    epub-utils extract book.epub --output-dir validation/
    # Run EPUBCheck on extracted content

    # Check specific components
    epub-utils manifest book.epub --format xml > manifest.xml
    epub-utils metadata book.epub --format xml > metadata.xml

Future Standards
================

EPUB 3.3 and Beyond
-------------------

Current developments in EPUB standards:

- **Enhanced accessibility features**
- **Better multimedia support**
- **Improved metadata vocabularies**
- **Web standards alignment**

Staying Current
---------------

- Monitor W3C EPUB Working Group
- Test with latest validators
- Follow accessibility guidelines (WCAG)
- Use semantic markup

Resources
=========

Official Specifications
-----------------------

- `EPUB 3.3 Specification <https://www.w3.org/TR/epub-33/>`_
- `EPUB Accessibility 1.1 <https://www.w3.org/TR/epub-a11y-11/>`_
- `EPUB Open Container Format 3.0.1 <https://www.w3.org/TR/epub-ocf-301/>`_

Validation Tools
----------------

- `EPUBCheck <https://github.com/w3c/epubcheck>`_
- `Ace Accessibility Checker <https://github.com/daisy/ace>`_
- `EPUB Validator <https://validator.idpf.org/>`_

Developer Resources
-------------------

- `EPUB 3 Best Practices <https://www.w3.org/TR/epub-bp/>`_
- `IDPF EPUB Resources <http://idpf.org/epub/31/spec/>`_
- `Accessibility Guidelines <https://www.w3.org/WAI/WCAG21/quickref/>`_
