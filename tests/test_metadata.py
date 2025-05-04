import pytest
from xml.etree import ElementTree as ET
from epub_utils.package.metadata import Metadata


VALID_METADATA_XML = """
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Test Book</dc:title>
    <dc:creator>Test Author</dc:creator>
    <dc:identifier>test-id-123</dc:identifier>
</metadata>
"""

INVALID_METADATA_XML = """
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Test Book</dc:title>
    <dc:creator>Test Author</dc:creator>
</metadata>
"""


def test_metadata_parse_valid_element():
    """Test parsing valid metadata XML."""
    metadata = Metadata(VALID_METADATA_XML)
    
    assert metadata.title == "Test Book"
    assert metadata.creator == "Test Author"
    assert metadata.identifier == "test-id-123"


def test_metadata_parse_missing_identifier():
    """Test that parsing metadata without identifier raises error."""
    with pytest.raises(ValueError, match="Invalid metadata element: Missing identifier."):
        Metadata(INVALID_METADATA_XML)
