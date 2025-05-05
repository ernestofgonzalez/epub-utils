try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

from epub_utils.exceptions import ParseError
from epub_utils.highlighters import highlight_xml


class Metadata:
    """
    Represents the metadata section of an EPUB package document.
    """

    DC_NAMESPACE = "http://purl.org/dc/elements/1.1/"
    TITLE_XPATH = f".//{{{DC_NAMESPACE}}}title"
    CREATOR_XPATH = f".//{{{DC_NAMESPACE}}}creator"
    IDENTIFIER_XPATH = f".//{{{DC_NAMESPACE}}}identifier"
    REQUIRED_FIELDS = ['identifier', 'title', 'creator']

    def __init__(self, xml_content: str):
        self.xml_content = xml_content 

        self.identifier = None
        self.title = None
        self.creator = None
        self.language = None
        self.subject = None
        self.description = None
        self.publisher = None
        self.date = None
        self.rights = None

        self._parse(xml_content)

    def _parse(self, xml_content: str) -> None:
        try:
            if isinstance(xml_content, str):
                xml_content = xml_content.encode("utf-8")
            root = etree.fromstring(xml_content)
            
            # Parse required metadata fields
            self.title = self._get_text(root, self.TITLE_XPATH)
            self.creator = self._get_text(root, self.CREATOR_XPATH)
            self.identifier = self._get_text(root, self.IDENTIFIER_XPATH)
            
            # Validate fields
            self._validate()
                
        except etree.ParseError as e:
            raise ParseError(f"Error parsing metadata element: {e}")
    
    def _validate(self, raise_exception=False) -> None:
        """
        Validate all required fields and raise ValueError if validation fails.
        """
        errors = {}
        
        for field in self.REQUIRED_FIELDS:
            try:
                self._validate_field(field)
            except ValueError as e:
                errors[field] = str(e)
        
        if errors and raise_exception:
            error_messages = [f"{field}: {msg}" for field, msg in errors.items()]
            # TODO: save validation errors for check functionality
            raise ValueError(f"Invalid metadata element: {', '.join(error_messages)}")

    def _validate_field(self, field_name: str) -> None:
        """
        Validate an individual field.
        
        Args:
            field_name: Name of the field to validate

        Raises:
            ValueError: If the field validation fails
        """
        value = getattr(self, field_name)
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError(f"This field is required")
    
    def __str__(self) -> str:
        return self.xml_content
    
    def to_str(self) -> str:
        return str(self)

    def to_xml(self, highlight_syntax=True) -> str:
        return highlight_xml(self.xml_content)

    def _get_text(self, root: etree.Element, xpath: str) -> str:
        """Extract text content from an XML element."""
        element = root.find(xpath)
        return element.text.strip() if element is not None and element.text else None

    def to_kv(self) -> str:
        """Format metadata as key-value pairs."""
        fields = [
            ("title", self.title),
            ("creator", self.creator), 
            ("identifier", self.identifier),
            ("language", self.language),
            ("subject", self.subject),
            ("description", self.description),
            ("publisher", self.publisher),
            ("date", self.date),
            ("rights", self.rights)
        ]
        return "\n".join(f"{k}: {v}" for k, v in fields if v is not None)
