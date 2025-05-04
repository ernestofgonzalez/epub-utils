from epub_utils.doc import Document
from epub_utils.container import Container
from epub_utils.package import Package
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
    doc = Document(doc_path)
    assert isinstance(doc.package, Package)

def test_document_toc(doc_path):
    """
    Test that the Document class correctly parses the table of contents file.
    """
    doc = Document(doc_path)
    assert isinstance(doc.toc, TableOfContents)
