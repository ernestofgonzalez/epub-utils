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


def test_ncx_navigation_interface():
	"""Test the new navigation interface methods."""
	ncx = NCXNavigation(NCX_XML, 'application/x-dtbncx+xml', 'toc.ncx')

	# Test get_toc_items
	toc_items = ncx.get_toc_items()
	assert len(toc_items) == 1

	item = toc_items[0]
	assert item.id == 'navpoint-1'
	assert item.label == 'Chapter 1'
	assert item.target == 'chapter1.xhtml'
	assert item.order == 1
	assert item.level == 0

	# Test get_page_list (should be empty for this sample)
	page_list = ncx.get_page_list()
	assert len(page_list) == 0

	# Test get_landmarks (should be empty for this sample)
	landmarks = ncx.get_landmarks()
	assert len(landmarks) == 0

	# Test find_item_by_id
	found_item = ncx.find_item_by_id('navpoint-1')
	assert found_item is not None
	assert found_item.label == 'Chapter 1'

	# Test find_items_by_target
	found_items = ncx.find_items_by_target('chapter1.xhtml')
	assert len(found_items) == 1
	assert found_items[0].id == 'navpoint-1'


def test_ncx_navigation_hierarchy():
	"""Test hierarchical navigation structure."""
	ncx_xml_hierarchical = """<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="en">
    <head>
        <meta name="dtb:uid" content="urn:uuid:12345"/>
        <meta name="dtb:depth" content="2"/>
        <meta name="dtb:totalPageCount" content="0"/>
        <meta name="dtb:maxPageNumber" content="0"/>
    </head>
    <docTitle>
        <text>Sample Book</text>
    </docTitle>
    <navMap>
        <navPoint id="ch1" playOrder="1">
            <navLabel>
                <text>Chapter 1</text>
            </navLabel>
            <content src="chapter1.xhtml"/>
            <navPoint id="ch1-1" playOrder="2">
                <navLabel>
                    <text>Section 1.1</text>
                </navLabel>
                <content src="chapter1.xhtml#section1"/>
            </navPoint>
        </navPoint>
        <navPoint id="ch2" playOrder="3">
            <navLabel>
                <text>Chapter 2</text>
            </navLabel>
            <content src="chapter2.xhtml"/>
        </navPoint>
    </navMap>
</ncx>"""

	ncx = NCXNavigation(ncx_xml_hierarchical, 'application/x-dtbncx+xml', 'toc.ncx')

	toc_items = ncx.get_toc_items_as_dicts()

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
					'order': 2,
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
			'order': 3,
			'level': 0,
			'type': None,
			'children': [],
		},
	]


def test_ncx_navigation_editing():
	"""Test the editing capabilities of the navigation interface."""
	from epub_utils.navigation.base import NavigationItem

	ncx = NCXNavigation(NCX_XML, 'application/x-dtbncx+xml', 'toc.ncx')

	# Test adding a new item
	new_item = NavigationItem(id='ch2', label='Chapter 2', target='chapter2.xhtml', order=2)

	ncx.add_toc_item(new_item)

	# Verify it was added
	toc_items = ncx.get_toc_items()
	assert len(toc_items) == 2

	new_toc_item = ncx.find_item_by_id('ch2')
	assert new_toc_item is not None
	assert new_toc_item.label == 'Chapter 2'

	# Test updating an item
	success = ncx.update_toc_item(
		'ch2', label='Chapter Two Updated', target='chapter2_updated.xhtml'
	)
	assert success

	updated_item = ncx.find_item_by_id('ch2')
	assert updated_item.label == 'Chapter Two Updated'
	assert updated_item.target == 'chapter2_updated.xhtml'

	# Test removing an item
	success = ncx.remove_toc_item('ch2')
	assert success

	# Verify it was removed
	toc_items = ncx.get_toc_items()
	assert len(toc_items) == 1
	assert ncx.find_item_by_id('ch2') is None
