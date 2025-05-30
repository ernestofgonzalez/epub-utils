import pytest

from epub_utils.package.manifest import Manifest

VALID_MANIFEST_XML = """
<manifest xmlns="http://www.idpf.org/2007/opf">
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="chapter1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
    <item id="style" href="style.css" media-type="text/css"/>
    <item id="image1" href="image1.jpg" media-type="image/jpeg"/>
</manifest>
"""

MINIMAL_MANIFEST_XML = """
<manifest xmlns="http://www.idpf.org/2007/opf">
    <item id="content" href="content.xhtml" media-type="application/xhtml+xml"/>
</manifest>
"""


def test_manifest_initialization():
	manifest = Manifest(VALID_MANIFEST_XML)

	assert len(manifest.items) == 4

	assert manifest.items[0]['id'] == 'nav'
	assert manifest.items[0]['href'] == 'nav.xhtml'
	assert manifest.items[0]['media_type'] == 'application/xhtml+xml'
	assert manifest.items[0]['properties'] == ['nav']

	assert manifest.items[2]['id'] == 'style'
	assert manifest.items[2]['href'] == 'style.css'
	assert manifest.items[2]['media_type'] == 'text/css'
	assert manifest.items[2]['properties'] == []


def test_minimal_manifest():
	manifest = Manifest(MINIMAL_MANIFEST_XML)

	assert len(manifest.items) == 1
	assert manifest.items[0]['id'] == 'content'
	assert manifest.items[0]['href'] == 'content.xhtml'
	assert manifest.items[0]['media_type'] == 'application/xhtml+xml'
	assert manifest.items[0]['properties'] == []


def test_find_by_property():
	manifest = Manifest(VALID_MANIFEST_XML)
	nav_item = manifest.find_by_property('nav')
	assert nav_item['id'] == 'nav'
	assert nav_item['href'] == 'nav.xhtml'


def test_find_by_id():
	manifest = Manifest(VALID_MANIFEST_XML)
	chapter = manifest.find_by_id('chapter1')
	assert chapter['href'] == 'chapter1.xhtml'
	assert chapter['media_type'] == 'application/xhtml+xml'


def test_find_by_media_type():
	manifest = Manifest(VALID_MANIFEST_XML)
	xhtml_items = manifest.find_by_media_type('application/xhtml+xml')
	assert len(xhtml_items) == 2
	assert all(item['media_type'] == 'application/xhtml+xml' for item in xhtml_items)


@pytest.mark.parametrize(
	'xml_content,pretty_print,expected',
	[
		(
			'<manifest xmlns="http://www.idpf.org/2007/opf">\n    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>\n\n    <item id="chapter1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>\n</manifest>',
			False,
			'<manifest xmlns="http://www.idpf.org/2007/opf">\n    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>\n\n    <item id="chapter1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>\n</manifest>',
		),
		(
			'<manifest xmlns="http://www.idpf.org/2007/opf">\n    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>\n\n    <item id="chapter1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>\n</manifest>',
			True,
			'<manifest xmlns="http://www.idpf.org/2007/opf">\n  <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>\n  <item id="chapter1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>\n</manifest>\n',
		),
	],
)
def test_manifest_to_str_pretty_print_parameter(xml_content, pretty_print, expected):
	"""Test XML output with and without pretty printing for Manifest."""
	manifest = Manifest(xml_content)

	assert manifest.to_str(pretty_print=pretty_print) == expected
