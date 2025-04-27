from setuptools import setup
import os

VERSION = "0.0.0a1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="epub_utils",
    description="A Python CLI and utility library for manipulating EPUB files",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Ernesto González",
    url="https://github.com/ernestofgonzalez/epub-utils",
    project_urls={
        "Issues": "https://github.com/ernestofgonzalez/epub-utils/issues",
        "CI": "https://github.com/ernestofgonzalez/epub-utils/actions",
        "Changelog": "https://github.com/ernestofgonzalez/epub-utils/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["epub_utils"],
    install_requires=[],
    extras_require={"test": ["pytest"]},
    python_requires=">=3.7",
)