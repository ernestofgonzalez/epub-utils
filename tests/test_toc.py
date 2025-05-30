import pytest

from epub_utils.toc import TableOfContents

NCX_TOC_XML = """<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
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

NAV_TOC_XML = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
    <head>
        <title>Navigation</title>
    </head>
    <body>
        <nav epub:type="toc">
            <h1>Table of Contents</h1>
            <ol>
                <li><a href="chapter1.xhtml">Chapter 1</a></li>
                <li><a href="chapter2.xhtml">Chapter 2</a></li>
            </ol>
        </nav>
    </body>
</html>"""


def test_toc_initialization_with_ncx():
	"""Test that the TableOfContents class initializes correctly with NCX content."""
	toc = TableOfContents(NCX_TOC_XML)
	assert toc is not None
	assert toc.xml_content == NCX_TOC_XML


def test_toc_initialization_with_nav():
	"""Test that the TableOfContents class initializes correctly with Navigation Document content."""
	toc = TableOfContents(NAV_TOC_XML)
	assert toc is not None
	assert toc.xml_content == NAV_TOC_XML


@pytest.mark.parametrize(
	'xml_content,pretty_print,expected',
	[
		(
			'<?xml version="1.0" encoding="UTF-8"?>\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n    <head>\n        <meta name="dtb:uid" content="urn:uuid:12345"/>\n    </head>\n\n    <docTitle>\n        <text>Sample Book</text>\n    </docTitle>\n</ncx>',
			False,
			'<?xml version="1.0" encoding="UTF-8"?>\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n    <head>\n        <meta name="dtb:uid" content="urn:uuid:12345"/>\n    </head>\n\n    <docTitle>\n        <text>Sample Book</text>\n    </docTitle>\n</ncx>',
		),
		(
			'<?xml version="1.0" encoding="UTF-8"?>\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n    <head>\n        <meta name="dtb:uid" content="urn:uuid:12345"/>\n    </head>\n\n    <docTitle>\n        <text>Sample Book</text>\n    </docTitle>\n</ncx>',
			True,
			'<?xml version="1.0" encoding="UTF-8"?>\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n  <head>\n    <meta name="dtb:uid" content="urn:uuid:12345"/>\n  </head>\n  <docTitle>\n    <text>Sample Book</text>\n  </docTitle>\n</ncx>\n',
		),
	],
)
def test_toc_to_str_pretty_print_parameter(xml_content, pretty_print, expected):
	"""Test XML output with and without pretty printing for TableOfContents."""
	toc = TableOfContents(xml_content)

	assert toc.to_str(pretty_print=pretty_print) == expected
