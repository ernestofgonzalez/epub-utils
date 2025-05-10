import pytest
from epub_utils.package import Package

VALID_OPF_XML = """<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:title>Sample EPUB</dc:title>
        <dc:creator>John Doe</dc:creator>
        <dc:identifier>12345</dc:identifier>
    </metadata>
    <manifest>
        <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    </manifest>
</package>
"""

INVALID_OPF_XML_MISSING_METADATA = """<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0">
</package>
"""

VALID_EPUB3_XML_WITHOUT_TOC = """<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:title>Sample EPUB</dc:title>
    </metadata>
</package>
"""

VALID_EPUB2_XML = """<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0">
<manifest><item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/></manifest>
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Sample EPUB</dc:title>
</metadata>
</package>
"""

VALID_EPUB2_XML_WITHOUT_TOC = """<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Sample EPUB</dc:title>
</metadata>
</package>
"""


def test_package_initialization():
    """
    Test that the Package class initializes correctly with valid OPF XML content.
    """
    package = Package(VALID_OPF_XML)
    assert package.metadata.title == "Sample EPUB"
    assert package.metadata.creator == "John Doe"
    assert package.metadata.identifier == "12345"


def test_package_invalid_xml():
    """
    Test that the Package class raises a ParseError for invalid XML content.
    """
    with pytest.raises(Exception, match="Invalid OPF file: Missing metadata element."):
        Package(INVALID_OPF_XML_MISSING_METADATA)


def test_epub3():
    package = Package(VALID_OPF_XML)
    assert package.version == "3.0"
    assert package.major_version == "3"
    assert package.nav_href == "nav.xhtml"


def test_epub3_without_toc():
    package = Package(VALID_EPUB3_XML_WITHOUT_TOC)
    assert package.version == "3.0"
    assert package.major_version == "3"
    assert not package.nav_href


def test_epub2():
    package = Package(VALID_EPUB2_XML)
    assert package.version == "2.0"
    assert package.major_version == "2"
    assert package.toc_href == "toc.ncx"


def test_epub2_without_toc():
    package = Package(VALID_EPUB2_XML_WITHOUT_TOC)
    assert package.version == "2.0"
    assert package.major_version == "2"
    assert not package.toc_href
