from pygments import highlight
from pygments.lexers import XmlLexer
from pygments.formatters import TerminalFormatter


def highlight_xml(xml_content: str) -> str:
    return highlight(xml_content, XmlLexer(), TerminalFormatter())