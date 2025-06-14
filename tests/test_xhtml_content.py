import pytest

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


@pytest.mark.parametrize(
	'xml_content,pretty_print,expected',
	[
		(
			'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n    <body>\n        <p>This is a simple paragraph.</p>\n\n    </body>\n</html>',
			False,
			'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n    <body>\n        <p>This is a simple paragraph.</p>\n\n    </body>\n</html>',
		),
		(
			'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n    <body>\n        <p>This is a simple paragraph.</p>\n\n    </body>\n</html>',
			True,
			'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n  <body>\n    <p>This is a simple paragraph.</p>\n  </body>\n</html>\n',
		),
		(
			'<?xml version="1.0" encoding="UTF-8"?>\n<html xmlns="http://www.w3.org/1999/xhtml">\n    <body>\n        <p>This is a simple paragraph.</p>\n\n    </body>\n</html>',
			False,
			'<?xml version="1.0" encoding="UTF-8"?>\n<html xmlns="http://www.w3.org/1999/xhtml">\n    <body>\n        <p>This is a simple paragraph.</p>\n\n    </body>\n</html>',
		),
		(
			'<?xml version="1.0" encoding="UTF-8"?>\n<html xmlns="http://www.w3.org/1999/xhtml">\n    <body>\n        <p>This is a simple paragraph.</p>\n\n    </body>\n</html>',
			True,
			'<?xml version="1.0" encoding="UTF-8"?>\n<html xmlns="http://www.w3.org/1999/xhtml">\n  <body>\n    <p>This is a simple paragraph.</p>\n  </body>\n</html>\n',
		),
		(
			'<html xmlns="http://www.w3.org/1999/xhtml">\n    <body>\n        <p>This is a simple paragraph.</p>\n\n    </body>\n</html>',
			False,
			'<html xmlns="http://www.w3.org/1999/xhtml">\n    <body>\n        <p>This is a simple paragraph.</p>\n\n    </body>\n</html>',
		),
		(
			'<html xmlns="http://www.w3.org/1999/xhtml">\n    <body>\n        <p>This is a simple paragraph.</p>\n\n    </body>\n</html>',
			True,
			'<html xmlns="http://www.w3.org/1999/xhtml">\n  <body>\n    <p>This is a simple paragraph.</p>\n  </body>\n</html>\n',
		),
	],
)
def test_to_str_pretty_print_parameter(xml_content, pretty_print, expected):
	"""Test XML output with and without pretty printing."""
	content = XHTMLContent(xml_content, 'application/xhtml+xml', 'test.xhtml')

	assert content.to_str(pretty_print=pretty_print) == expected
