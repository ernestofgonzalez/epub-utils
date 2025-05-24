from epub_utils.content.xhtml import XHTMLContent


def test_simple_paragraph():
	"""Test extraction from a simple paragraph."""
	xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <html xmlns="http://www.w3.org/1999/xhtml">
        <body>
            <p>This is a simple paragraph.</p>
        </body>
    </html>"""

	content = XHTMLContent(xml_content, 'application/xhtml+xml', 'test.xhtml')

	assert content.inner_text == 'This is a simple paragraph.'
