import pytest

from epub_utils.container import Container

CONTAINER_XML = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>
"""


def test_container_initialization():
	"""
	Test that the Container class initializes correctly with valid XML content.
	"""
	container = Container(CONTAINER_XML)
	assert container is not None
	assert container.rootfile_path == 'OEBPS/content.opf'


def test_invalid_container_xml():
	"""
	Test that the Container class raises an error for invalid XML content.
	"""
	invalid_xml = '<invalid></invalid>'
	with pytest.raises(
		ValueError, match='Invalid container.xml: Missing rootfile element or full-path attribute.'
	):
		Container(invalid_xml)
