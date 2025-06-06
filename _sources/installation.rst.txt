Installation Guide
==================

System Requirements
-------------------

``epub-utils`` requires Python 3.10 or higher and works on:

- **Linux** (Ubuntu 18.04+, Debian 10+, CentOS 7+, Fedora 30+)
- **macOS** (10.14+)
- **Windows** (Windows 10+)

Installing from PyPI
---------------------

The easiest way to install ``epub-utils`` is using pip:

.. code-block:: bash

   $ pip install epub-utils

This will install the latest stable version with all required dependencies.

Development Installation
------------------------

If you want to contribute to ``epub-utils`` or use the latest development version:

.. code-block:: bash

   # Clone the repository
   $ git clone https://github.com/ernestofgonzalez/epub-utils.git
   $ cd epub-utils

   # Create a virtual environment
   $ python -m venv env
   $ source env/bin/activate  # On Windows: env\Scripts\activate

   # Install in development mode
   $ pip install -e .

   # Install development dependencies
   $ pip install -r requirements/requirements-testing.txt
   $ pip install -r requirements/requirements-linting.txt

Virtual Environment Installation
--------------------------------

For isolated installations, we recommend using virtual environments:

Using venv (Python 3.3+)
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Create virtual environment
   $ python -m venv epub-utils-env

   # Activate virtual environment
   $ source epub-utils-env/bin/activate  # Linux/macOS
   $ epub-utils-env\Scripts\activate     # Windows

   # Install epub-utils
   $ pip install epub-utils

Using conda
~~~~~~~~~~~

.. code-block:: bash

   # Create conda environment
   $ conda create -n epub-utils python=3.10

   # Activate environment
   $ conda activate epub-utils

   # Install epub-utils
   $ pip install epub-utils

Verifying Installation
----------------------

After installation, verify that ``epub-utils`` is working correctly:

.. code-block:: bash

   # Check version
   $ epub-utils --version

   # Test with a sample EPUB (if you have one)
   $ epub-utils sample.epub metadata

If you see the version number and can run commands without errors, the installation was successful!

Installing from Source
----------------------

To install from source code:

.. code-block:: bash

   # Download and extract the source
   $ wget https://github.com/ernestofgonzalez/epub-utils/archive/main.zip
   $ unzip main.zip
   $ cd epub-utils-main

   # Install
   $ pip install .

Upgrading
---------

To upgrade to the latest version:

.. code-block:: bash

   $ pip install --upgrade epub-utils

Uninstalling
------------

To remove epub-utils:

.. code-block:: bash

   $ pip uninstall epub-utils

Performance Considerations
--------------------------

Installing lxml
~~~~~~~~~~~~~~~

While not required, installing ``lxml`` can significantly improve XML parsing performance:

.. code-block:: bash

   $ pip install lxml

``epub-utils`` will automatically use lxml if available, falling back to the standard library's 
``xml.etree.ElementTree`` if not.

