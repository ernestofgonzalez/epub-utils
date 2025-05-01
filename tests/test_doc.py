from epub_utils.doc import Document
from epub_utils.container import Container
from epub_utils.package import Package


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
