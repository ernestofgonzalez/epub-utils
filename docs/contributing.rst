============
Contributing
============

We welcome contributions to ``epub-utils``! This guide will help you get started with contributing to the project.

Getting Started
===============

Setting Up Development Environment
----------------------------------

1. **Fork the Repository**

   Fork the ``epub-utils`` repository on GitHub to your own account.

2. **Clone Your Fork**

   .. code-block:: bash

       git clone https://github.com/yourusername/epub-utils.git
       cd epub-utils

3. **Set Up Development Environment**

   .. code-block:: bash

       # Create virtual environment
       python -m venv dev-env
       source dev-env/bin/activate  # On Windows: dev-env\Scripts\activate
       
       # Install in development mode
       pip install -e ".[dev]"
       
       # Or install dependencies manually
       pip install -e .
       pip install pytest black flake8 mypy sphinx


Project Structure
-----------------

.. code-block:: text

    epub-utils/
    ├── src/
    │   └── epub_utils/
    │       ├── __init__.py
    │       ├── cli.py              # Command-line interface
    │       ├── document.py         # Main Document class
    │       ├── extractors.py       # Content extraction logic
    │       └── formatters.py       # Output formatting
    ├── tests/
    │   ├── __init__.py
    │   ├── test_document.py
    │   ├── test_cli.py
    │   └── fixtures/               # Test EPUB files
    ├── docs/
    │   ├── conf.py
    │   ├── index.rst
    │   └── ...                     # Documentation files
    ├── pyproject.toml
    ├── README.md
    └── CHANGELOG.md

Development Workflow
====================

Branch Strategy
---------------

- ``main`` branch: Stable, release-ready code
- ``develop`` branch: Integration branch for features
- Feature branches: ``feature/your-feature-name``
- Bug fix branches: ``fix/issue-description``

Making Changes
--------------

1. **Create a Feature Branch**

   .. code-block:: bash

       git checkout -b feature/your-feature-name

2. **Make Your Changes**

   Follow the coding standards outlined below.

3. **Write Tests**

   All new features should include comprehensive tests.

4. **Run Tests Locally**

   .. code-block:: bash

       # Run all tests
       pytest
       
       # Run with coverage
       pytest --cov=epub_utils
       
       # Run specific test file
       pytest tests/test_document.py

5. **Check Code Quality**

   .. code-block:: bash

       # Format code
       black src/ tests/
       
       # Check linting
       flake8 src/ tests/
       
       # Type checking
       mypy src/

6. **Update Documentation**

   If your changes affect the API or add new features, update the documentation.

7. **Commit Your Changes**

   .. code-block:: bash

       git add .
       git commit -m "Add: Brief description of your changes"

8. **Push and Create Pull Request**

   .. code-block:: bash

       git push origin feature/your-feature-name

   Then create a pull request on GitHub.

Coding Standards
================

Python Style Guide
------------------

We follow PEP 8 with some modifications:

- **Line length**: 88 characters (Black's default)
- **String quotes**: Use double quotes for strings
- **Import sorting**: Use isort or similar tool
- **Docstrings**: Use Google-style docstrings

Code Formatting
---------------

We use **Black** for code formatting:

.. code-block:: bash

    # Format all Python files
    black src/ tests/
    
    # Check formatting without making changes
    black --check src/ tests/

Example of properly formatted code:

.. code-block:: python

    def extract_metadata(epub_path: str, format_type: str = "dict") -> dict:
        """Extract metadata from an EPUB file.
        
        Args:
            epub_path: Path to the EPUB file.
            format_type: Output format ('dict', 'xml', 'json').
            
        Returns:
            Dictionary containing extracted metadata.
            
        Raises:
            FileNotFoundError: If the EPUB file doesn't exist.
            ValueError: If format_type is not supported.
        """
        if not os.path.exists(epub_path):
            raise FileNotFoundError(f"EPUB file not found: {epub_path}")
        
        if format_type not in ["dict", "xml", "json"]:
            raise ValueError(f"Unsupported format: {format_type}")
        
        # Implementation here...
        return {}

Linting
-------

We use **flake8** for linting:

.. code-block:: bash

    # Check for linting errors
    flake8 src/ tests/
    
    # Configuration in setup.cfg or pyproject.toml
    [flake8]
    max-line-length = 88
    extend-ignore = E203, W503

Type Hints
----------

Use type hints for all function signatures:

.. code-block:: python

    from typing import List, Dict, Optional, Union
    from pathlib import Path

    def process_files(
        file_paths: List[Union[str, Path]], 
        output_format: str = "table"
    ) -> Optional[Dict[str, any]]:
        """Process multiple EPUB files."""
        pass

Documentation Standards
=======================

Docstring Format
----------------

Use Google-style docstrings:

.. code-block:: python

    def complex_function(param1: str, param2: int, param3: bool = False) -> dict:
        """Brief description of the function.
        
        Longer description if needed. Explain the purpose, behavior,
        and any important details about the function.
        
        Args:
            param1: Description of the first parameter.
            param2: Description of the second parameter.
            param3: Description of optional parameter. Defaults to False.
            
        Returns:
            Description of return value and its structure.
            
        Raises:
            ValueError: When param2 is negative.
            FileNotFoundError: When the specified file doesn't exist.
            
        Example:
            Basic usage example:
            
            >>> result = complex_function("test", 42)
            >>> print(result["status"])
            "success"
        """
        pass

API Documentation
-----------------

When adding new classes or functions to the public API:

1. **Add to __init__.py** exports if appropriate
2. **Update API reference** documentation
3. **Include usage examples** in docstrings
4. **Add to tutorials** if it's a major feature

RST Documentation
-----------------

When writing RST documentation:

.. code-block:: rst

    Section Title
    =============
    
    Subsection
    ----------
    
    Code examples:
    
    .. code-block:: python
    
        # Python code here
        import epub_utils
        
    Shell commands:
    
    .. code-block:: bash
    
        epub-utils info book.epub

Testing Guidelines
==================

Test Structure
--------------

- **Unit tests**: Test individual functions and methods
- **Integration tests**: Test component interactions
- **End-to-end tests**: Test complete workflows
- **Performance tests**: Test with large files (optional)

Writing Tests
-------------

Use pytest for all tests:

.. code-block:: python

    import pytest
    from epub_utils import Document
    from pathlib import Path

    class TestDocument:
        """Test Document class functionality."""
        
        def setup_method(self):
            """Set up test fixtures."""
            self.test_epub = Path("tests/fixtures/sample.epub")
            
        def test_document_creation(self):
            """Test creating a Document instance."""
            doc = Document(str(self.test_epub))
            assert doc is not None
            assert len(doc.metadata) > 0
            
        def test_document_with_invalid_file(self):
            """Test error handling with invalid file."""
            with pytest.raises(FileNotFoundError):
                Document("nonexistent.epub")
                
        @pytest.mark.parametrize("format_type", ["dict", "xml", "json"])
        def test_metadata_formats(self, format_type):
            """Test different metadata formats."""
            doc = Document(str(self.test_epub))
            metadata = doc.get_metadata(format_type=format_type)
            assert metadata is not None

Test Fixtures
-------------

Create test EPUB files in ``tests/fixtures/``:

.. code-block:: python

    # tests/conftest.py
    import pytest
    from pathlib import Path

    @pytest.fixture
    def sample_epub():
        """Provide path to sample EPUB for testing."""
        return Path(__file__).parent / "fixtures" / "sample.epub"
        
    @pytest.fixture
    def invalid_epub():
        """Provide path to invalid EPUB for error testing."""
        return Path(__file__).parent / "fixtures" / "invalid.epub"

Running Tests
-------------

.. code-block:: bash

    # Run all tests
    pytest
    
    # Run with verbose output
    pytest -v
    
    # Run specific test file
    pytest tests/test_document.py
    
    # Run specific test
    pytest tests/test_document.py::TestDocument::test_document_creation
    
    # Run with coverage
    pytest --cov=epub_utils --cov-report=html

Types of Contributions
======================

Bug Reports
-----------

When reporting bugs:

1. **Check existing issues** first
2. **Use the issue template** if available
3. **Provide minimal reproduction case**
4. **Include system information**

.. code-block:: text

    **Bug Description**
    Clear description of the bug.
    
    **Steps to Reproduce**
    1. Step one
    2. Step two
    3. Step three
    
    **Expected Behavior**
    What should happen.
    
    **Actual Behavior**
    What actually happens.
    
    **Environment**
    - epub-utils version: 
    - Python version:
    - Operating system:
    
    **Sample File**
    Attach or link to EPUB file if relevant.

Feature Requests
----------------

For new features:

1. **Describe the use case** clearly
2. **Explain why it's valuable** to users
3. **Suggest implementation approach** if you have ideas
4. **Consider backward compatibility**

Documentation Improvements
--------------------------

Documentation contributions are highly valued:

- **Fix typos** and grammar errors
- **Improve clarity** of explanations
- **Add more examples** to existing docs
- **Create new tutorials** for common use cases
- **Update outdated information**

Code Contributions
------------------

Areas where contributions are welcome:

1. **Performance improvements**
2. **New output formats**
3. **Additional EPUB validation**
4. **Better error handling**
5. **CLI usability enhancements**
6. **Support for EPUB 3 features**

Release Process
===============

Versioning
----------

We follow `Semantic Versioning <https://semver.org/>`_:

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Version format: ``MAJOR.MINOR.PATCH`` (e.g., ``1.2.3``)

Development versions may include additional identifiers:
- ``1.2.3-dev`` (development)
- ``1.2.3rc1`` (release candidate)

Changelog
---------

Update ``CHANGELOG.md`` with:

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerabilities

Example entry:

.. code-block:: markdown

    ## [1.2.0] - 2024-05-25
    
    ### Added
    - New `--batch` option for processing multiple files
    - Support for EPUB 3.3 navigation documents
    - JSON output format for metadata
    
    ### Fixed
    - Handle corrupted ZIP files gracefully
    - Fix Unicode encoding issues on Windows
    
    ### Changed
    - Improved error messages for invalid EPUB files

Community Guidelines
====================

Code of Conduct
---------------

We are committed to providing a welcoming and inclusive environment:

- **Be respectful** and considerate
- **Be collaborative** and helpful
- **Focus on what's best** for the project and community
- **Show empathy** towards other community members

Communication
-------------

- **GitHub Issues**: Bug reports and feature requests
- **Pull Requests**: Code review and discussion
- **Documentation**: Examples and tutorials

Recognition
-----------

Contributors will be recognized in:

- **CHANGELOG.md**: For significant contributions
- **README.md**: In the contributors section
- **Release notes**: For major features

Getting Help
============

If you need help with contributing:

1. **Check this guide** first
2. **Look at existing issues** and pull requests
3. **Ask questions** in GitHub issues
4. **Start with small contributions** to get familiar

Mentorship
----------

New contributors are welcome! If you're new to open source:

- **Start with documentation** improvements
- **Look for "good first issue"** labels
- **Ask for guidance** - maintainers are happy to help
- **Don't be afraid** to make mistakes

Thank You!
==========

Every contribution, no matter how small, helps make ``epub-utils`` better for everyone. Whether you're fixing a typo, reporting a bug, or implementing a new feature, your efforts are appreciated!

Happy contributing!
