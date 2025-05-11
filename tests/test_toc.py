from epub_utils.doc import Document
from epub_utils.container import Container
from epub_utils.package import Package
from epub_utils.toc import TableOfContents


EPUB3_TOC = """<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">
  <head>
    <meta charset="utf-8"/>
  </head>
  <body>
    <nav epub:type="toc" id="toc">
      <ol>
        <li id="front">
          <a href="Roads.xhtml">Roads</a>
        </li>
      </ol>
    </nav>
  </body>
</html>
"""


EPUB2_TOC = """<?xml version='1.0' encoding='utf-8'?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="deu">
  <docTitle>
    <text>Example</text>
  </docTitle>
  <navMap>
    <navPoint id="navPoint-0" playOrder="1">
      <navLabel>
        <text>Start</text>
      </navLabel>
      <content src="titlepage.xhtml"/>
    </navPoint>
    <navPoint id="navPoint-1" playOrder="2">
      <navLabel>
        <text>Chapter 1</text>
      </navLabel>
      <content src="chapter1.xhtml"/>
      <navPoint id="navPoint-1.1" playOrder="3">
        <navLabel>
          <text>Section 1.1</text>
        </navLabel>
        <content src="chapter1.xhtml#section1.1"/>
      </navPoint>
    </navPoint>
  </navMap>
</ncx>
"""


def test_toc_epub3(doc_path):
    """
    Test that the Document class correctly parses the table of contents file.
    """
    toc = TableOfContents(EPUB3_TOC, major_version=3)
    assert 1 == len(toc)
    assert [{'label': 'Roads', 'path': 'Roads.xhtml'}] == list(toc)


def test_toc_epub2(doc_path):
    """
    Test that the Document class correctly parses the table of contents file.
    """
    toc = TableOfContents(EPUB2_TOC, major_version=2)
    assert 3 == len(toc)
    expected = [
        {'label': 'Start', 'path': 'titlepage.xhtml'},
        {'label': 'Chapter 1', 'path': 'chapter1.xhtml'},
        {'label': 'Section 1.1', 'path': 'chapter1.xhtml#section1.1'},
    ]
    assert expected == list(toc)
