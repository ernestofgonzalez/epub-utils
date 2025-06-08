"""
Tests for NCX DOM.
"""

from lxml import etree

from epub_utils.navigation.ncx.dom import NCXDocument

NCX_XML = """<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="en-US">
    <head>
        <meta name="dtb:uid" content="org-example-5059463624137734586"/>
        <meta name="dtb:depth" content="2"/>
        <meta name="dtb:totalPageCount" content="100"/>
        <meta name="dtb:maxPageNumber" content="100"/>
    </head>
    <docTitle>
        <text>Selections from "Great Pictures, As Seen and Described by Famous Writers"</text>
    </docTitle>
    <docAuthor>
        <text>Esther Singleton</text>
    </docAuthor>
    <navMap>
        <navPoint class="h1" id="ch1" playOrder="1">
            <navLabel>
                <text>Chapter 1</text>
            </navLabel>
            <content src="content.html#ch_1"/>
            <navPoint class="h2" id="ch_1_1" playOrder="2">
                <navLabel>
                    <text>Chapter 1.1</text>
                </navLabel>
                <content src="content.html#ch_1_1"/>
            </navPoint>
        </navPoint>
        <navPoint class="h1" id="ch2" playOrder="3">
            <navLabel>
                <text>Chapter 2</text>
            </navLabel>
            <content src="content.html#ch_2"/>
        </navPoint>
    </navMap>
    <pageList>
        <pageTarget id="p1" type="normal" value="1" playOrder="1">
            <navLabel><text>1</text></navLabel>
            <content src="content.html#p1"/>
        </pageTarget>
        <pageTarget id="p2" type="normal" value="2" playOrder="2">
            <navLabel><text>2</text></navLabel>
            <content src="content.html#p2"/>
        </pageTarget>
    </pageList>
    <navList>
        <navLabel>
            <text>List of Illustrations</text>
        </navLabel>
        <navTarget id="ill-1">
            <navLabel><text>Portrait of Georg Gisze (Holbein)</text></navLabel>
            <content src="content.html#ill1"/>
        </navTarget>
        <navTarget id="ill-2">
            <navLabel><text>The adoration of the lamb (Van Eyck)</text></navLabel>
            <content src="content.html#ill2"/>
        </navTarget>
    </navList>
</ncx>"""


def test_ncx_document_parsing():
	"""Test that NCXDocument correctly parses the XML string into DOM tree."""
	# Parse the XML
	tree = etree.fromstring(NCX_XML.encode('utf-8'))
	ncx_doc = NCXDocument(tree)

	# Test root element attributes
	assert ncx_doc.version == '2005-1'
	assert ncx_doc.lang == 'en-US'


def test_ncx_document_head():
	"""Test that the head element and its meta tags are correctly parsed."""
	tree = etree.fromstring(NCX_XML.encode('utf-8'))
	ncx_doc = NCXDocument(tree)

	head = ncx_doc.head
	assert head is not None

	# Test meta elements
	metas = head.metas
	assert len(metas) == 4

	# Test specific meta values
	uid_meta = head.get_meta('dtb:uid')
	assert uid_meta is not None
	assert uid_meta.content == 'org-example-5059463624137734586'

	depth_meta = head.get_meta('dtb:depth')
	assert depth_meta is not None
	assert depth_meta.content == '2'

	page_count_meta = head.get_meta('dtb:totalPageCount')
	assert page_count_meta is not None
	assert page_count_meta.content == '100'

	max_page_meta = head.get_meta('dtb:maxPageNumber')
	assert max_page_meta is not None
	assert max_page_meta.content == '100'


def test_ncx_document_title_and_author():
	"""Test that docTitle and docAuthor elements are correctly parsed."""
	tree = etree.fromstring(NCX_XML.encode('utf-8'))
	ncx_doc = NCXDocument(tree)

	# Test document title
	doc_title = ncx_doc.doc_title
	assert doc_title is not None
	assert (
		doc_title.text
		== 'Selections from "Great Pictures, As Seen and Described by Famous Writers"'
	)
	assert (
		ncx_doc.title == 'Selections from "Great Pictures, As Seen and Described by Famous Writers"'
	)

	# Test document author
	doc_author = ncx_doc.doc_author
	assert doc_author is not None
	assert doc_author.text == 'Esther Singleton'
	assert ncx_doc.author == 'Esther Singleton'


def test_ncx_document_nav_map():
	"""Test that the navMap and navPoint elements are correctly parsed."""
	tree = etree.fromstring(NCX_XML.encode('utf-8'))
	ncx_doc = NCXDocument(tree)

	nav_map = ncx_doc.nav_map
	assert nav_map is not None

	# Test top-level nav points
	nav_points = nav_map.nav_points
	assert len(nav_points) == 2

	# Test first nav point (Chapter 1)
	ch1 = nav_points[0]
	assert ch1.id == 'ch1'
	assert ch1.class_attr == 'h1'
	assert ch1.play_order == 1
	assert ch1.label_text == 'Chapter 1'
	assert ch1.content_src == 'content.html#ch_1'

	# Test nested nav point (Chapter 1.1)
	ch1_children = ch1.nav_points
	assert len(ch1_children) == 1
	ch1_1 = ch1_children[0]
	assert ch1_1.id == 'ch_1_1'
	assert ch1_1.class_attr == 'h2'
	assert ch1_1.play_order == 2
	assert ch1_1.label_text == 'Chapter 1.1'
	assert ch1_1.content_src == 'content.html#ch_1_1'

	# Test second nav point (Chapter 2)
	ch2 = nav_points[1]
	assert ch2.id == 'ch2'
	assert ch2.class_attr == 'h1'
	assert ch2.play_order == 3
	assert ch2.label_text == 'Chapter 2'
	assert ch2.content_src == 'content.html#ch_2'

	# Test that Chapter 2 has no children
	assert len(ch2.nav_points) == 0

	# Test get_all_nav_points method
	all_nav_points = nav_map.get_all_nav_points()
	assert len(all_nav_points) == 3  # ch1, ch_1_1, ch2


def test_ncx_document_page_list():
	"""Test that the pageList and pageTarget elements are correctly parsed."""
	tree = etree.fromstring(NCX_XML.encode('utf-8'))
	ncx_doc = NCXDocument(tree)

	page_list = ncx_doc.page_list
	assert page_list is not None

	page_targets = page_list.page_targets
	assert len(page_targets) == 2

	# Test first page target
	p1 = page_targets[0]
	assert p1.id == 'p1'
	assert p1.type_attr == 'normal'
	assert p1.value == '1'
	assert p1.play_order == 1
	assert p1.label_text == '1'
	assert p1.content_src == 'content.html#p1'

	# Test second page target
	p2 = page_targets[1]
	assert p2.id == 'p2'
	assert p2.type_attr == 'normal'
	assert p2.value == '2'
	assert p2.play_order == 2
	assert p2.label_text == '2'
	assert p2.content_src == 'content.html#p2'


def test_ncx_document_nav_list():
	"""Test that the navList and navTarget elements are correctly parsed."""
	tree = etree.fromstring(NCX_XML.encode('utf-8'))
	ncx_doc = NCXDocument(tree)

	nav_lists = ncx_doc.nav_lists
	assert len(nav_lists) == 1

	nav_list = nav_lists[0]
	assert nav_list.label_text == 'List of Illustrations'

	nav_targets = nav_list.nav_targets
	assert len(nav_targets) == 2

	# Test first nav target
	ill1 = nav_targets[0]
	assert ill1.id == 'ill-1'
	assert ill1.label_text == 'Portrait of Georg Gisze (Holbein)'
	assert ill1.content_src == 'content.html#ill1'

	# Test second nav target
	ill2 = nav_targets[1]
	assert ill2.id == 'ill-2'
	assert ill2.label_text == 'The adoration of the lamb (Van Eyck)'
	assert ill2.content_src == 'content.html#ill2'


def test_ncx_document_convenience_methods():
	"""Test the convenience methods for extracting metadata."""
	tree = etree.fromstring(NCX_XML.encode('utf-8'))
	ncx_doc = NCXDocument(tree)

	# Test UID extraction
	assert ncx_doc.get_uid() == 'org-example-5059463624137734586'

	# Test depth extraction
	assert ncx_doc.get_depth() == 2

	# Test page count extraction
	assert ncx_doc.get_total_page_count() == 100

	# Test max page number extraction
	assert ncx_doc.get_max_page_number() == 100


def test_ncx_nav_label_content_access():
	"""Test accessing navLabel and content elements directly."""
	tree = etree.fromstring(NCX_XML.encode('utf-8'))
	ncx_doc = NCXDocument(tree)

	nav_map = ncx_doc.nav_map
	nav_point = nav_map.nav_points[0]  # Chapter 1

	# Test navLabel access
	nav_label = nav_point.nav_label
	assert nav_label is not None
	text_element = nav_label.text_element
	assert text_element is not None
	assert text_element.text == 'Chapter 1'

	# Test content access
	content = nav_point.content
	assert content is not None
	assert content.src == 'content.html#ch_1'


def test_ncx_document_with_minimal_xml():
	"""Test NCXDocument with minimal valid NCX XML."""
	minimal_ncx = """<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
    <head>
        <meta name="dtb:uid" content="test-uid"/>
    </head>
    <docTitle>
        <text>Test Book</text>
    </docTitle>
    <navMap>
        <navPoint id="ch1" playOrder="1">
            <navLabel>
                <text>Chapter 1</text>
            </navLabel>
            <content src="ch1.html"/>
        </navPoint>
    </navMap>
</ncx>"""

	tree = etree.fromstring(minimal_ncx.encode('utf-8'))
	ncx_doc = NCXDocument(tree)

	# Test basic parsing
	assert ncx_doc.version == '2005-1'
	assert ncx_doc.title == 'Test Book'
	assert ncx_doc.get_uid() == 'test-uid'

	# Test nav map
	nav_map = ncx_doc.nav_map
	assert nav_map is not None
	nav_points = nav_map.nav_points
	assert len(nav_points) == 1
	assert nav_points[0].label_text == 'Chapter 1'

	# Test optional elements are None when not present
	assert ncx_doc.doc_author is None
	assert ncx_doc.author == ''
	assert ncx_doc.page_list is None
	assert len(ncx_doc.nav_lists) == 0


def test_ncx_element_attribute_access():
	"""Test getting and setting attributes on NCX elements."""
	tree = etree.fromstring(NCX_XML.encode('utf-8'))
	ncx_doc = NCXDocument(tree)

	nav_point = ncx_doc.nav_map.nav_points[0]

	# Test getting attributes
	assert nav_point.get_attribute('id') == 'ch1'
	assert nav_point.get_attribute('class') == 'h1'
	assert nav_point.get_attribute('playOrder') == '1'
	assert nav_point.get_attribute('nonexistent') is None

	# Test setting attributes
	nav_point.set_attribute('custom-attr', 'test-value')
	assert nav_point.get_attribute('custom-attr') == 'test-value'


def test_ncx_document_missing_elements():
	"""Test behavior when optional elements are missing."""
	minimal_ncx = """<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
    <head>
        <meta name="dtb:uid" content="test-uid"/>
    </head>
    <navMap>
    </navMap>
</ncx>"""

	tree = etree.fromstring(minimal_ncx.encode('utf-8'))
	ncx_doc = NCXDocument(tree)

	# Test missing elements return None or empty values
	assert ncx_doc.doc_title is None
	assert ncx_doc.title == ''
	assert ncx_doc.doc_author is None
	assert ncx_doc.author == ''
	assert ncx_doc.page_list is None
	assert len(ncx_doc.nav_lists) == 0

	# Test missing meta elements return None
	assert ncx_doc.get_depth() is None
	assert ncx_doc.get_total_page_count() is None
	assert ncx_doc.get_max_page_number() is None
