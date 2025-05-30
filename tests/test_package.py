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

VALID_OEPBS1_XML_WITH_TOC = """<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" version="1.0">
<manifest><item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/></manifest>
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Sample EPUB</dc:title>
</metadata>
</package>
"""

INVALID_VERSION = """<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" version="4.0">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" />
</package>
"""


def test_package_initialization():
	"""
	Test that the Package class initializes correctly with valid OPF XML content.
	"""
	package = Package(VALID_OPF_XML)
	assert package.metadata.title == 'Sample EPUB'
	assert package.metadata.creator == 'John Doe'
	assert package.metadata.identifier == '12345'


def test_package_invalid_xml():
	"""
	Test that the Package class raises a ParseError for invalid XML content.
	"""
	with pytest.raises(Exception, match='Invalid OPF file: Missing metadata element.'):
		Package(INVALID_OPF_XML_MISSING_METADATA)


def test_epub3():
	package = Package(VALID_OPF_XML)
	assert package.version.public == '3.0'
	assert package.version.major == 3
	assert package.nav_href == 'nav.xhtml'


def test_epub3_without_toc():
	package = Package(VALID_EPUB3_XML_WITHOUT_TOC)
	assert package.version.public == '3.0'
	assert package.version.major == 3
	assert not package.nav_href


def test_epub2():
	package = Package(VALID_EPUB2_XML)
	assert package.version.public == '2.0'
	assert package.version.major == 2
	assert package.toc_href == 'toc.ncx'


def test_epub2_without_toc():
	package = Package(VALID_EPUB2_XML_WITHOUT_TOC)
	assert package.version.public == '2.0'
	assert package.version.major == 2
	assert not package.toc_href


def test_epub1():
	package = Package(VALID_OEPBS1_XML_WITH_TOC)
	assert package.version.public == '1.0'
	assert package.version.major == 1
	assert package.toc_href == 'toc.ncx'


def test_invalid_version():
	with pytest.raises(ValueError, match='Unsupported epub version: 4'):
		package = Package(INVALID_VERSION)


@pytest.mark.parametrize(
	'xml_content,pretty_print,expected',
	[
		(
			'<?xml version="1.0"?>\n<package xmlns="http://www.idpf.org/2007/opf" version="3.0">\n\n    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n\n        <dc:title>Sample EPUB</dc:title>\n    </metadata>\n</package>',
			False,
			'<?xml version="1.0"?>\n<package xmlns="http://www.idpf.org/2007/opf" version="3.0">\n\n    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n\n        <dc:title>Sample EPUB</dc:title>\n    </metadata>\n</package>',
		),
		(
			'<?xml version="1.0"?>\n<package xmlns="http://www.idpf.org/2007/opf" version="3.0">\n\n    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n\n        <dc:title>Sample EPUB</dc:title>\n    </metadata>\n</package>',
			True,
			'<?xml version="1.0"?>\n<package xmlns="http://www.idpf.org/2007/opf" version="3.0">\n  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n    <dc:title>Sample EPUB</dc:title>\n  </metadata>\n</package>\n',
		),
	],
)
def test_package_to_str_pretty_print_parameter(xml_content, pretty_print, expected):
	"""Test XML output with and without pretty printing for Package."""
	package = Package(xml_content)

	assert package.to_str(pretty_print=pretty_print) == expected
