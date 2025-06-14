import pytest

from epub_utils.package.spine import Spine

VALID_SPINE_XML = """
<spine xmlns="http://www.idpf.org/2007/opf" toc="ncx" page-progression-direction="ltr">
    <itemref idref="cover" linear="no"/>
    <itemref idref="nav" linear="yes"/>
    <itemref idref="chapter1" properties="page-spread-left"/>
    <itemref idref="chapter2"/>
</spine>
"""

MINIMAL_SPINE_XML = """
<spine xmlns="http://www.idpf.org/2007/opf">
    <itemref idref="content"/>
</spine>
"""


def test_spine_initialization():
	spine = Spine(VALID_SPINE_XML)

	assert spine.toc == 'ncx'
	assert spine.page_progression_direction == 'ltr'
	assert len(spine.itemrefs) == 4

	# Test first itemref (cover)
	assert spine.itemrefs[0]['idref'] == 'cover'
	assert spine.itemrefs[0]['linear'] == False
	assert spine.itemrefs[0]['properties'] == []

	# Test third itemref (chapter1)
	assert spine.itemrefs[2]['idref'] == 'chapter1'
	assert spine.itemrefs[2]['linear'] == True
	assert spine.itemrefs[2]['properties'] == ['page-spread-left']


def test_minimal_spine():
	spine = Spine(MINIMAL_SPINE_XML)

	assert spine.toc is None
	assert spine.page_progression_direction == 'default'
	assert len(spine.itemrefs) == 1
	assert spine.itemrefs[0]['idref'] == 'content'
	assert spine.itemrefs[0]['linear'] == True
	assert spine.itemrefs[0]['properties'] == []


@pytest.mark.parametrize(
	'xml_content,pretty_print,expected',
	[
		(
			'<spine xmlns="http://www.idpf.org/2007/opf" toc="ncx">\n\n    <itemref idref="cover" linear="no"/>\n\n    <itemref idref="chapter1"/>\n</spine>',
			False,
			'<spine xmlns="http://www.idpf.org/2007/opf" toc="ncx">\n\n    <itemref idref="cover" linear="no"/>\n\n    <itemref idref="chapter1"/>\n</spine>',
		),
		(
			'<spine xmlns="http://www.idpf.org/2007/opf" toc="ncx">\n\n    <itemref idref="cover" linear="no"/>\n\n    <itemref idref="chapter1"/>\n</spine>',
			True,
			'<spine xmlns="http://www.idpf.org/2007/opf" toc="ncx">\n  <itemref idref="cover" linear="no"/>\n  <itemref idref="chapter1"/>\n</spine>\n',
		),
	],
)
def test_spine_to_str_pretty_print_parameter(xml_content, pretty_print, expected):
	"""Test XML output with and without pretty printing for Spine."""
	spine = Spine(xml_content)

	assert spine.to_str(pretty_print=pretty_print) == expected
