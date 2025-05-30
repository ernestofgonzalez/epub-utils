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


@pytest.mark.parametrize(
	'xml_content,pretty_print,expected',
	[
		(
			'<?xml version="1.0"?>\n<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n    <rootfiles>\n\n        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n    </rootfiles>\n</container>',
			False,
			'<?xml version="1.0"?>\n<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n    <rootfiles>\n\n        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n    </rootfiles>\n</container>',
		),
		(
			'<?xml version="1.0"?>\n<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n    <rootfiles>\n\n        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n    </rootfiles>\n</container>',
			True,
			'<?xml version="1.0"?>\n<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">\n  <rootfiles>\n    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n  </rootfiles>\n</container>\n',
		),
	],
)
def test_container_to_str_pretty_print_parameter(xml_content, pretty_print, expected):
	"""Test XML output with and without pretty printing for Container."""
	container = Container(xml_content)

	assert container.to_str(pretty_print=pretty_print) == expected
