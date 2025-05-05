import pytest
from epub_utils.package import Package

VALID_OPF_XML = """<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:title>Sample EPUB</dc:title>
        <dc:creator>John Doe</dc:creator>
        <dc:identifier>12345</dc:identifier>
    </metadata>
</package>
"""

INVALID_OPF_XML_MISSING_METADATA = """<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0">
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
