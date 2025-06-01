import os

from setuptools import find_packages, setup

VERSION = '0.0.0a5'


def get_long_description():
	with open(
		os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md'),
		encoding='utf8',
	) as fp:
		return fp.read()


setup(
	name='epub-utils',
	description='A Python CLI and utility library for manipulating EPUB files',
	long_description=get_long_description(),
	long_description_content_type='text/markdown',
	author='Ernesto González',
	url='https://github.com/ernestofgonzalez/epub-utils',
	project_urls={
		'Source code': 'https://github.com/ernestofgonzalez/epub-utils',
		'Issues': 'https://github.com/ernestofgonzalez/epub-utils/issues',
		'CI': 'https://github.com/ernestofgonzalez/epub-utils/actions',
		'Changelog': 'https://github.com/ernestofgonzalez/epub-utils/releases',
	},
	license='Apache License, Version 2.0',
	version=VERSION,
	packages=find_packages(),
	entry_points={
		'console_scripts': [
			'epub-utils = epub_utils.cli:main',
		]
	},
	install_requires=[
		'click',
		'lxml',
		'packaging',
		'pygments',
		'PyYAML',
	],
	extras_require={
		'test': ['pytest'],
		'docs': [
			'sphinx',
			'sphinx-copybutton',
			'sphinx-issues',
			'furo',
		],
	},
	python_requires='>=3.10',
	classifiers=[
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Libraries',
		'Topic :: Utilities',
		'Programming Language :: Python :: 3.10',
		'Programming Language :: Python :: 3.11',
		'Programming Language :: Python :: 3.12',
		'Programming Language :: Python :: 3.13',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: POSIX',
		'Operating System :: Unix',
		'Operating System :: MacOS',
	],
)
