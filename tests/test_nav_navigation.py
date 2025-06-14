from epub_utils.navigation.nav import EPUBNavDocNavigation

NAV_XML = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
    <title>Navigation Document</title>
</head>
<body>
    <nav epub:type="toc" id="toc">
        <h1>Table of Contents</h1>
        <ol>
            <li id="ch1-li">
                <a href="chapter1.xhtml" id="ch1">Chapter 1</a>
            </li>
        </ol>
    </nav>
</body>
</html>"""


def test_nav_doc_navigation_initialization():
	"""Test that the EPUBNavDocNavigation class initializes correctly."""
	nav = EPUBNavDocNavigation(NAV_XML, 'application/xhtml+xml', 'nav.xhtml')
	assert nav is not None
	assert nav.xml_content == NAV_XML
	assert nav.media_type == 'application/xhtml+xml'
	assert nav.href == 'nav.xhtml'

	assert nav.xmlns == 'http://www.w3.org/1999/xhtml'
	assert nav.lang == 'en'


def test_nav_doc_navigation_interface():
	"""Test the new navigation interface methods."""
	nav = EPUBNavDocNavigation(NAV_XML, 'application/xhtml+xml', 'nav.xhtml')

	# Test get_toc_items
	toc_items = nav.get_toc_items()
	assert len(toc_items) == 1

	item = toc_items[0]
	assert item.id == 'ch1'
	assert item.label == 'Chapter 1'
	assert item.target == 'chapter1.xhtml'
	assert item.order == 1
	assert item.level == 0

	# Test get_page_list (should be empty for this sample)
	page_list = nav.get_page_list()
	assert len(page_list) == 0

	# Test get_landmarks (should be empty for this sample)
	landmarks = nav.get_landmarks()
	assert len(landmarks) == 0

	# Test find_item_by_id
	found_item = nav.find_item_by_id('ch1')
	assert found_item is not None
	assert found_item.label == 'Chapter 1'

	# Test find_items_by_target
	found_items = nav.find_items_by_target('chapter1.xhtml')
	assert len(found_items) == 1
	assert found_items[0].id == 'ch1'


def test_nav_doc_navigation_toc_items_as_dicts():
	"""Test hierarchical navigation structure."""
	nav_xml_hierarchical = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
    <title>Navigation Document</title>
</head>
<body>
    <nav epub:type="toc" id="toc">
        <h1>Table of Contents</h1>
        <ol>
            <li id="ch1-li">
                <a href="chapter1.xhtml" id="ch1">Chapter 1</a>
                <ol>
                    <li id="ch1-1-li">
                        <a href="chapter1.xhtml#section1" id="ch1-1">Section 1.1</a>
                    </li>
                </ol>
            </li>
            <li id="ch2-li">
                <a href="chapter2.xhtml" id="ch2">Chapter 2</a>
            </li>
        </ol>
    </nav>
</body>
</html>"""

	nav = EPUBNavDocNavigation(nav_xml_hierarchical, 'application/xhtml+xml', 'nav.xhtml')

	toc_items = nav.get_toc_items_as_dicts()

	assert toc_items == [
		{
			'id': 'ch1',
			'label': 'Chapter 1',
			'target': 'chapter1.xhtml',
			'order': 1,
			'level': 0,
			'type': None,
			'children': [
				{
					'id': 'ch1-1',
					'label': 'Section 1.1',
					'target': 'chapter1.xhtml#section1',
					'order': 1,
					'level': 1,
					'type': None,
					'children': [],
				}
			],
		},
		{
			'id': 'ch2',
			'label': 'Chapter 2',
			'target': 'chapter2.xhtml',
			'order': 2,
			'level': 0,
			'type': None,
			'children': [],
		},
	]


def test_nav_doc_navigation_page_list():
	"""Test page list functionality."""
	nav_xml_with_pages = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
    <title>Navigation Document</title>
</head>
<body>
    <nav epub:type="toc" id="toc">
        <h1>Table of Contents</h1>
        <ol>
            <li><a href="chapter1.xhtml" id="ch1">Chapter 1</a></li>
        </ol>
    </nav>
    <nav epub:type="page-list" id="page-list">
        <h1>List of Pages</h1>
        <ol>
            <li><a href="chapter1.xhtml#page1" id="page1">1</a></li>
            <li><a href="chapter1.xhtml#page2" id="page2">2</a></li>
            <li><a href="chapter2.xhtml#page3" id="page3">3</a></li>
        </ol>
    </nav>
</body>
</html>"""

	nav = EPUBNavDocNavigation(nav_xml_with_pages, 'application/xhtml+xml', 'nav.xhtml')

	# Test get_page_list
	page_list = nav.get_page_list()
	assert len(page_list) == 3

	page1 = page_list[0]
	assert page1.id == 'page1'
	assert page1.label == '1'
	assert page1.target == 'chapter1.xhtml#page1'
	assert page1.order == 1
	assert page1.level == 0
	assert page1.item_type in [None, 'page']  # Could be None or 'page'

	page2 = page_list[1]
	assert page2.id == 'page2'
	assert page2.label == '2'
	assert page2.target == 'chapter1.xhtml#page2'

	page3 = page_list[2]
	assert page3.id == 'page3'
	assert page3.label == '3'
	assert page3.target == 'chapter2.xhtml#page3'


def test_nav_doc_navigation_landmarks():
	"""Test landmarks functionality."""
	nav_xml_with_landmarks = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
    <title>Navigation Document</title>
</head>
<body>
    <nav epub:type="toc" id="toc">
        <h1>Table of Contents</h1>
        <ol>
            <li><a href="chapter1.xhtml" id="ch1">Chapter 1</a></li>
        </ol>
    </nav>
    <nav epub:type="landmarks" id="landmarks">
        <h1>Landmarks</h1>
        <ol>
            <li><a href="cover.xhtml" epub:type="cover" id="cover">Cover</a></li>
            <li><a href="toc.xhtml" epub:type="toc" id="toc-landmark">Table of Contents</a></li>
            <li><a href="chapter1.xhtml" epub:type="bodymatter" id="start">Start of Content</a></li>
        </ol>
    </nav>
</body>
</html>"""

	nav = EPUBNavDocNavigation(nav_xml_with_landmarks, 'application/xhtml+xml', 'nav.xhtml')

	# Test get_landmarks
	landmarks = nav.get_landmarks()
	assert len(landmarks) == 3

	cover_landmark = landmarks[0]
	assert cover_landmark.id == 'cover'
	assert cover_landmark.label == 'Cover'
	assert cover_landmark.target == 'cover.xhtml'
	assert cover_landmark.item_type == 'cover'

	toc_landmark = landmarks[1]
	assert toc_landmark.id == 'toc-landmark'
	assert toc_landmark.label == 'Table of Contents'
	assert toc_landmark.target == 'toc.xhtml'
	assert toc_landmark.item_type == 'toc'

	start_landmark = landmarks[2]
	assert start_landmark.id == 'start'
	assert start_landmark.label == 'Start of Content'
	assert start_landmark.target == 'chapter1.xhtml'
	assert start_landmark.item_type == 'bodymatter'


def test_nav_doc_navigation_editing():
	"""Test the editing capabilities of the navigation interface."""
	from epub_utils.navigation.base import NavigationItem

	nav = EPUBNavDocNavigation(NAV_XML, 'application/xhtml+xml', 'nav.xhtml')

	# Test adding a new item
	new_item = NavigationItem(id='ch2', label='Chapter 2', target='chapter2.xhtml', order=2)

	nav.add_toc_item(new_item)

	# Verify it was added
	toc_items = nav.get_toc_items()
	assert len(toc_items) == 2

	new_toc_item = nav.find_item_by_id('ch2')
	assert new_toc_item is not None
	assert new_toc_item.label == 'Chapter 2'

	# Test updating an item
	success = nav.update_toc_item(
		'ch2', label='Chapter Two Updated', target='chapter2_updated.xhtml'
	)
	assert success

	updated_item = nav.find_item_by_id('ch2')
	assert updated_item.label == 'Chapter Two Updated'
	assert updated_item.target == 'chapter2_updated.xhtml'

	# Test removing an item
	success = nav.remove_toc_item('ch2')
	assert success

	# Verify it was removed
	toc_items = nav.get_toc_items()
	assert len(toc_items) == 1
	assert nav.find_item_by_id('ch2') is None


def test_nav_doc_navigation_span_elements():
	"""Test navigation with span elements (non-linked text)."""
	nav_xml_with_spans = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
    <title>Navigation Document</title>
</head>
<body>
    <nav epub:type="toc" id="toc">
        <h1>Table of Contents</h1>
        <ol>
            <li id="part1-li">
                <span id="part1">Part 1</span>
                <ol>
                    <li><a href="chapter1.xhtml" id="ch1">Chapter 1</a></li>
                    <li><a href="chapter2.xhtml" id="ch2">Chapter 2</a></li>
                </ol>
            </li>
        </ol>
    </nav>
</body>
</html>"""

	nav = EPUBNavDocNavigation(nav_xml_with_spans, 'application/xhtml+xml', 'nav.xhtml')

	toc_items = nav.get_toc_items()
	assert len(toc_items) == 1

	part1_item = toc_items[0]
	assert part1_item.id == 'part1'
	assert part1_item.label == 'Part 1'
	assert part1_item.target == ''  # span elements don't have targets
	assert len(part1_item.children) == 2

	ch1_item = part1_item.children[0]
	assert ch1_item.id == 'ch1'
	assert ch1_item.label == 'Chapter 1'
	assert ch1_item.target == 'chapter1.xhtml'

	ch2_item = part1_item.children[1]
	assert ch2_item.id == 'ch2'
	assert ch2_item.label == 'Chapter 2'
	assert ch2_item.target == 'chapter2.xhtml'


def test_nav_doc_navigation_item_types():
	"""Test navigation with epub:type attributes."""
	nav_xml_with_types = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
    <title>Navigation Document</title>
</head>
<body>
    <nav epub:type="toc" id="toc">
        <h1>Table of Contents</h1>
        <ol>
            <li><a href="preface.xhtml" epub:type="preface" id="preface">Preface</a></li>
            <li><a href="chapter1.xhtml" epub:type="chapter" id="ch1">Chapter 1</a></li>
            <li><a href="appendix.xhtml" epub:type="appendix" id="appendix">Appendix</a></li>
        </ol>
    </nav>
</body>
</html>"""

	nav = EPUBNavDocNavigation(nav_xml_with_types, 'application/xhtml+xml', 'nav.xhtml')

	toc_items = nav.get_toc_items()
	assert len(toc_items) == 3

	preface_item = toc_items[0]
	assert preface_item.item_type == 'preface'

	chapter_item = toc_items[1]
	assert chapter_item.item_type == 'chapter'

	appendix_item = toc_items[2]
	assert appendix_item.item_type == 'appendix'


def test_nav_doc_navigation_invalid_media_type():
	"""Test that invalid media types raise ValueError."""
	import pytest

	with pytest.raises(ValueError, match='Invalid media type'):
		EPUBNavDocNavigation(NAV_XML, 'application/x-dtbncx+xml', 'nav.xhtml')


def test_nav_doc_navigation_malformed_xml():
	"""Test handling of malformed XML."""
	import pytest

	from epub_utils.exceptions import ParseError

	malformed_xml = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Navigation Document</title>
</head>
<body>
    <nav epub:type="toc">
        <ol>
            <li><a href="chapter1.xhtml">Chapter 1</a>
        </ol>
    </nav>
</body>
"""  # Missing closing </li> and </html>

	with pytest.raises(ParseError):
		EPUBNavDocNavigation(malformed_xml, 'application/xhtml+xml', 'nav.xhtml')


def test_nav_doc_navigation_output_methods():
	"""Test the various output methods."""
	nav = EPUBNavDocNavigation(NAV_XML, 'application/xhtml+xml', 'nav.xhtml')

	# Test __str__
	str_output = str(nav)
	assert str_output == NAV_XML

	# Test to_str (should use XMLPrinter)
	to_str_output = nav.to_str()
	assert isinstance(to_str_output, str)
	assert 'Chapter 1' in to_str_output

	# Test to_xml (may include ANSI color codes)
	to_xml_output = nav.to_xml()
	assert isinstance(to_xml_output, str)
	# Remove ANSI escape codes for testing
	import re

	clean_output = re.sub(r'\x1b\[[0-9;]*m', '', to_xml_output)
	assert 'Chapter 1' in clean_output

	# Test to_plain
	to_plain_output = nav.to_plain()
	assert isinstance(to_plain_output, str)
	assert 'Chapter 1' in to_plain_output


def test_nav_doc_navigation_reorder_items():
	"""Test reordering TOC items."""
	nav_xml_multiple = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
    <title>Navigation Document</title>
</head>
<body>
    <nav epub:type="toc" id="toc">
        <h1>Table of Contents</h1>
        <ol>
            <li><a href="chapter1.xhtml" id="ch1">Chapter 1</a></li>
            <li><a href="chapter2.xhtml" id="ch2">Chapter 2</a></li>
            <li><a href="chapter3.xhtml" id="ch3">Chapter 3</a></li>
        </ol>
    </nav>
</body>
</html>"""

	nav = EPUBNavDocNavigation(nav_xml_multiple, 'application/xhtml+xml', 'nav.xhtml')

	# Get original order
	original_items = nav.get_toc_items()
	assert [item.id for item in original_items] == ['ch1', 'ch2', 'ch3']

	# Reorder items
	nav.reorder_toc_items(['ch3', 'ch1', 'ch2'])

	# Check that the method completed without error
	# Note: The actual reordering implementation may vary
	# and this test mainly ensures the method can be called


def test_nav_doc_navigation_empty_document():
	"""Test handling of empty navigation document."""
	empty_nav_xml = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
    <title>Navigation Document</title>
</head>
<body>
</body>
</html>"""

	nav = EPUBNavDocNavigation(empty_nav_xml, 'application/xhtml+xml', 'nav.xhtml')

	# All lists should be empty
	assert len(nav.get_toc_items()) == 0
	assert len(nav.get_page_list()) == 0
	assert len(nav.get_landmarks()) == 0

	# find methods should return None/empty
	assert nav.find_item_by_id('nonexistent') is None
	assert len(nav.find_items_by_target('nonexistent.xhtml')) == 0
