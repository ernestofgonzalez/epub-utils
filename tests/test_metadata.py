import pytest

from epub_utils.package.metadata import Metadata

VALID_METADATA_XML = """
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/">
    <dc:title>Test Book</dc:title>
    <dc:creator>Test Author</dc:creator>
    <dc:identifier>test-id-123</dc:identifier>
    <dc:language>en</dc:language>
    <dc:subject>Fiction</dc:subject>
    <dc:subject>Science Fiction</dc:subject>
    <dc:date>2024-01-01</dc:date>
    <dc:publisher>Test Publisher</dc:publisher>
    <meta property="dcterms:modified">2023-11-28T14:50:13Z</meta>
    <meta property="dcterms:source">Original Source</meta>
</metadata>
"""

INVALID_METADATA_XML = """
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Test Book</dc:title>
    <dc:creator>Test Author</dc:creator>
</metadata>
"""


def test_metadata_parse_valid_element():
	"""Test parsing valid metadata XML with both required and optional DC terms."""
	metadata = Metadata(VALID_METADATA_XML)

	assert metadata.title == 'Test Book'
	assert metadata.creator == 'Test Author'
	assert metadata.identifier == 'test-id-123'

	assert metadata.language == 'en'
	assert metadata.subject == ['Fiction', 'Science Fiction']
	assert metadata.date == '2024-01-01'
	assert metadata.publisher == 'Test Publisher'

	assert metadata.modified == '2023-11-28T14:50:13Z'
	assert metadata.source == 'Original Source'


def test_metadata_validate_missing_identifier_with_raise_exception():
	"""Test that parsing metadata without identifier raises error."""
	with pytest.raises(
		ValueError, match='Invalid metadata element: identifier: This field is required'
	):
		Metadata(INVALID_METADATA_XML)._validate(raise_exception=True)
