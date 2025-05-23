import unittest

from epub_utils.container import Container
from epub_utils.doc import Document
from epub_utils.package import Manifest, Package
from epub_utils.toc import TableOfContents


def test_document_container(doc_path):
	"""
	Test that the Document class correctly parses the container.xml file.
	"""
	doc = Document(doc_path)
	assert isinstance(doc.container, Container)


def test_document_package(doc_path):
	"""
	Test that the Document class correctly parses the package file.
	"""
	case = unittest.TestCase()

	doc = Document(doc_path)
	assert isinstance(doc.package, Package)
	assert isinstance(doc.package.manifest, Manifest)
	case.assertCountEqual(
		doc.package.manifest.items,
		[
			{
				'id': 'toc',
				'href': 'nav.xhtml',
				'media_type': 'application/xhtml+xml',
				'properties': ['nav'],
			},
			{
				'id': 'main',
				'href': 'Roads.xhtml',
				'media_type': 'application/xhtml+xml',
				'properties': [],
			},
		],
	)


def test_document_toc(doc_path):
	"""
	Test that the Document class correctly parses the table of contents file.
	"""
	doc = Document(doc_path)
	assert isinstance(doc.toc, TableOfContents)


def test_document_find_content_by_id(doc_path):
	doc = Document(doc_path)
	content = doc.find_content_by_id('main')
	assert content is not None
