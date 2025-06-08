from epub_utils.navigation.ncx import NCXNavigation

NCX_XML = """<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="en">
    <head>
        <meta name="dtb:uid" content="urn:uuid:12345"/>
        <meta name="dtb:depth" content="1"/>
        <meta name="dtb:totalPageCount" content="0"/>
        <meta name="dtb:maxPageNumber" content="0"/>
    </head>
    <docTitle>
        <text>Sample Book</text>
    </docTitle>
    <navMap>
        <navPoint id="navpoint-1" playOrder="1">
            <navLabel>
                <text>Chapter 1</text>
            </navLabel>
            <content src="chapter1.xhtml"/>
        </navPoint>
    </navMap>
</ncx>"""


def test_ncx_navigation_initialization():
	"""Test that the NCXNavigation class initializes correctly."""
	ncx = NCXNavigation(NCX_XML, 'application/x-dtbncx+xml', 'toc.ncx')
	assert ncx is not None
	assert ncx.xml_content == NCX_XML
	assert ncx.media_type == 'application/x-dtbncx+xml'
	assert ncx.href == 'toc.ncx'

	assert ncx.xmlns == 'http://www.daisy.org/z3986/2005/ncx/'
	assert ncx.version == '2005-1'
	assert ncx.lang == 'en'
