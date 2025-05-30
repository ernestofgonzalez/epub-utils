Examples and Use Cases
======================

This page showcases real-world examples of using epub-utils for various tasks. Each example 
includes both CLI and Python API approaches where applicable.

Digital Library Management
--------------------------

Cataloging Your EPUB Collection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario**: You have a large collection of EPUB files and want to create a comprehensive catalog.

**CLI Approach**:

.. code-block:: bash

   #!/bin/bash
   # catalog-epubs.sh - Create a catalog of all EPUB files

   echo "Creating EPUB catalog..."
   echo "File,Title,Author,Publisher,Language,Year,Files,Size" > epub_catalog.csv

   find . -name "*.epub" -type f | while read -r epub; do
       echo "Processing: $epub"
       
       # Extract metadata using epub-utils
       metadata=$(epub-utils "$epub" metadata --format kv 2>/dev/null)
       
       if [ $? -eq 0 ]; then
           title=$(echo "$metadata" | grep "^title:" | cut -d' ' -f2- | sed 's/,/;/g')
           author=$(echo "$metadata" | grep "^creator:" | cut -d' ' -f2- | sed 's/,/;/g')
           publisher=$(echo "$metadata" | grep "^publisher:" | cut -d' ' -f2- | sed 's/,/;/g')
           language=$(echo "$metadata" | grep "^language:" | cut -d' ' -f2-)
           year=$(echo "$metadata" | grep "^date:" | cut -d' ' -f2- | cut -d'-' -f1)
           
           # Count files and get size
           file_count=$(epub-utils "$epub" files --format raw 2>/dev/null | wc -l)
           size=$(stat -f%z "$epub" 2>/dev/null || stat -c%s "$epub" 2>/dev/null)
           
           echo "$epub,$title,$author,$publisher,$language,$year,$file_count,$size" >> epub_catalog.csv
       else
           echo "$epub,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR" >> epub_catalog.csv
       fi
   done

   echo "Catalog complete! See epub_catalog.csv"

**Python Approach**:

.. code-block:: python

   import csv
   import os
   from pathlib import Path
   from epub_utils import Document

   def create_epub_catalog(directory, output_file="epub_catalog.csv"):
       """Create a comprehensive catalog of EPUB files."""
       
       fieldnames = [
           'filepath', 'filename', 'title', 'author', 'publisher', 
           'language', 'year', 'isbn', 'file_count', 'size_bytes', 'size_mb'
       ]
       
       epub_files = list(Path(directory).rglob("*.epub"))
       print(f"Found {len(epub_files)} EPUB files")
       
       with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
           writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
           writer.writeheader()
           
           for i, epub_path in enumerate(epub_files, 1):
               print(f"Processing {i}/{len(epub_files)}: {epub_path.name}")
               
               try:
                   doc = Document(str(epub_path))
                   metadata = doc.package.metadata
                   
                   # Extract date year
                   date_str = getattr(metadata, 'date', '')
                   year = date_str.split('-')[0] if date_str else ''
                   
                   # Get file size
                   size_bytes = epub_path.stat().st_size
                   size_mb = round(size_bytes / (1024 * 1024), 2)
                   
                   row = {
                       'filepath': str(epub_path),
                       'filename': epub_path.name,
                       'title': getattr(metadata, 'title', ''),
                       'author': getattr(metadata, 'creator', ''),
                       'publisher': getattr(metadata, 'publisher', ''),
                       'language': getattr(metadata, 'language', ''),
                       'year': year,
                       'isbn': getattr(metadata, 'identifier', ''),
                       'file_count': len(doc.get_files_info()),
                       'size_bytes': size_bytes,
                       'size_mb': size_mb
                   }
                   
                   writer.writerow(row)
                   
               except Exception as e:
                   print(f"  Error: {e}")
                   # Write error row
                   writer.writerow({
                       'filepath': str(epub_path),
                       'filename': epub_path.name,
                       'title': f'ERROR: {str(e)}',
                       'author': '',
                       'publisher': '',
                       'language': '',
                       'year': '',
                       'isbn': '',
                       'file_count': 0,
                       'size_bytes': epub_path.stat().st_size,
                       'size_mb': 0
                   })

   # Usage
   create_epub_catalog("/path/to/your/epub/collection")

Quality Assurance and Validation
---------------------------------

EPUB Health Check
~~~~~~~~~~~~~~~~~

**Scenario**: Validate EPUB files and identify potential issues.

.. code-block:: python

   from epub_utils import Document, ParseError
   import zipfile
   from pathlib import Path

   class EPUBHealthChecker:
       def __init__(self):
           self.issues = []
           
       def check_epub(self, epub_path):
           """Comprehensive EPUB health check."""
           self.issues = []
           epub_path = Path(epub_path)
           
           print(f"Checking EPUB: {epub_path.name}")
           
           # Basic file checks
           if not epub_path.exists():
               self.issues.append("File does not exist")
               return self.get_report()
           
           if epub_path.stat().st_size == 0:
               self.issues.append("File is empty")
               return self.get_report()
           
           # ZIP integrity check
           try:
               with zipfile.ZipFile(epub_path, 'r') as zf:
                   corrupt_files = zf.testzip()
                   if corrupt_files:
                       self.issues.append(f"Corrupt ZIP file: {corrupt_files}")
           except zipfile.BadZipFile:
               self.issues.append("Invalid ZIP file")
               return self.get_report()
           
           # EPUB structure checks
           try:
               doc = Document(str(epub_path))
               self._check_container(doc)
               self._check_package(doc)
               self._check_metadata(doc)
               self._check_manifest(doc)
               self._check_files(doc)
               
           except ParseError as e:
               self.issues.append(f"Parse error: {e}")
           except Exception as e:
               self.issues.append(f"Unexpected error: {e}")
           
           return self.get_report()
       
       def _check_container(self, doc):
           """Check container structure."""
           try:
               container = doc.container
               if not container.rootfile_path:
                   self.issues.append("No rootfile specified in container")
           except Exception as e:
               self.issues.append(f"Container error: {e}")
       
       def _check_package(self, doc):
           """Check package/OPF file."""
           try:
               package = doc.package
               if not hasattr(package, 'metadata'):
                   self.issues.append("Package missing metadata")
               if not hasattr(package, 'manifest'):
                   self.issues.append("Package missing manifest")
               if not hasattr(package, 'spine'):
                   self.issues.append("Package missing spine")
           except Exception as e:
               self.issues.append(f"Package error: {e}")
       
       def _check_metadata(self, doc):
           """Check metadata quality."""
           try:
               metadata = doc.package.metadata
               
               # Check required fields
               if not getattr(metadata, 'title', '').strip():
                   self.issues.append("Missing or empty title")
               if not getattr(metadata, 'language', '').strip():
                   self.issues.append("Missing or empty language")
               if not getattr(metadata, 'identifier', '').strip():
                   self.issues.append("Missing or empty identifier")
                   
           except Exception as e:
               self.issues.append(f"Metadata error: {e}")
       
       def _check_manifest(self, doc):
           """Check manifest integrity."""
           try:
               manifest = doc.package.manifest
               if not manifest.items:
                   self.issues.append("Empty manifest")
               
               # Check for common content types
               has_html = any(
                   item.get('media-type') == 'application/xhtml+xml'
                   for item in manifest.items.values()
               )
               if not has_html:
                   self.issues.append("No XHTML content files found")
                   
           except Exception as e:
               self.issues.append(f"Manifest error: {e}")
       
       def _check_files(self, doc):
           """Check file structure."""
           try:
               files_info = doc.get_files_info()
               if len(files_info) < 3:  # At least container, package, and one content file
                   self.issues.append("Very few files in EPUB (possibly incomplete)")
               
               # Check for suspiciously large files
               for file_info in files_info:
                   if file_info['size'] > 10 * 1024 * 1024:  # 10MB
                       self.issues.append(f"Large file found: {file_info['path']} ({file_info['size']} bytes)")
                       
           except Exception as e:
               self.issues.append(f"File check error: {e}")
       
       def get_report(self):
           """Generate health check report."""
           if not self.issues:
               return {"status": "healthy", "issues": []}
           else:
               return {"status": "issues_found", "issues": self.issues}

   # Usage
   checker = EPUBHealthChecker()
   report = checker.check_epub("book.epub")

   if report["status"] == "healthy":
       print("✓ EPUB is healthy!")
   else:
       print("⚠ Issues found:")
       for issue in report["issues"]:
           print(f"  - {issue}")

Metadata Management
-------------------

Standardizing Metadata
~~~~~~~~~~~~~~~~~~~~~~

**Scenario**: Clean and standardize metadata across your EPUB collection.

.. code-block:: python

   import re
   from epub_utils import Document

   class MetadataStandardizer:
       def __init__(self):
           self.language_codes = {
               'english': 'en',
               'spanish': 'es', 
               'french': 'fr',
               'german': 'de',
               'italian': 'it'
               # Add more as needed
           }
       
       def analyze_metadata(self, epub_path):
           """Analyze and suggest metadata improvements."""
           doc = Document(epub_path)
           metadata = doc.package.metadata
           suggestions = []
           
           # Check title
           title = getattr(metadata, 'title', '')
           if not title:
               suggestions.append("Missing title")
           elif len(title) > 200:
               suggestions.append("Title is very long (>200 chars)")
           elif title.isupper():
               suggestions.append("Title is all uppercase - consider title case")
           
           # Check author
           creator = getattr(metadata, 'creator', '')
           if not creator:
               suggestions.append("Missing author/creator")
           elif ',' not in creator and len(creator.split()) > 2:
               suggestions.append("Author name might need reformatting (Last, First)")
           
           # Check language
           language = getattr(metadata, 'language', '')
           if not language:
               suggestions.append("Missing language code")
           elif len(language) > 3:
               # Might be full language name instead of code
               lang_lower = language.lower()
               if lang_lower in self.language_codes:
                   suggestions.append(f"Use language code '{self.language_codes[lang_lower]}' instead of '{language}'")
           
           # Check identifier
           identifier = getattr(metadata, 'identifier', '')
           if not identifier:
               suggestions.append("Missing identifier")
           elif not self._is_valid_identifier(identifier):
               suggestions.append("Identifier format might be invalid")
           
           # Check date format
           date = getattr(metadata, 'date', '')
           if date and not re.match(r'\d{4}(-\d{2}-\d{2})?', date):
               suggestions.append("Date should be in YYYY or YYYY-MM-DD format")
           
           return {
               'file': epub_path,
               'current_metadata': {
                   'title': title,
                   'creator': creator,
                   'language': language,
                   'identifier': identifier,
                   'date': date
               },
               'suggestions': suggestions
           }
       
       def _is_valid_identifier(self, identifier):
           """Check if identifier looks valid."""
           # Check for ISBN, DOI, UUID patterns
           patterns = [
               r'urn:isbn:\d{10,13}',  # ISBN URN
               r'isbn:\d{10,13}',      # Simple ISBN
               r'urn:uuid:[a-f0-9-]{36}',  # UUID URN
               r'doi:10\.\d+/.+',      # DOI
               r'urn:doi:10\.\d+/.+'   # DOI URN
           ]
           
           return any(re.match(pattern, identifier, re.I) for pattern in patterns)

   # Usage
   standardizer = MetadataStandardizer()
   analysis = standardizer.analyze_metadata("book.epub")

   print(f"Analyzing: {analysis['file']}")
   if analysis['suggestions']:
       print("Suggestions for improvement:")
       for suggestion in analysis['suggestions']:
           print(f"  - {suggestion}")
   else:
       print("Metadata looks good!")

Content Analysis and Statistics
-------------------------------

Reading Level Analysis
~~~~~~~~~~~~~~~~~~~~~~

**Scenario**: Analyze EPUB content to determine reading complexity.

.. code-block:: python

   import re
   import math
   from epub_utils import Document

   class ReadingLevelAnalyzer:
       def analyze_epub(self, epub_path):
           """Analyze reading level of an EPUB."""
           doc = Document(epub_path)
           
           # Get all text content
           all_text = self._extract_all_text(doc)
           
           if not all_text.strip():
               return {"error": "No readable text found"}
           
           # Calculate statistics
           stats = self._calculate_text_stats(all_text)
           
           # Calculate reading level scores
           flesch_score = self._flesch_reading_ease(stats)
           flesch_grade = self._flesch_kincaid_grade(stats)
           
           return {
               'title': getattr(doc.package.metadata, 'title', 'Unknown'),
               'word_count': stats['words'],
               'sentence_count': stats['sentences'],
               'syllable_count': stats['syllables'],
               'avg_words_per_sentence': round(stats['words'] / stats['sentences'], 2),
               'avg_syllables_per_word': round(stats['syllables'] / stats['words'], 2),
               'flesch_reading_ease': round(flesch_score, 2),
               'flesch_kincaid_grade': round(flesch_grade, 2),
               'reading_level': self._interpret_flesch_score(flesch_score)
           }
       
       def _extract_all_text(self, doc):
           """Extract all readable text from EPUB."""
           # This is a simplified version - real implementation would
           # need to parse XHTML content files
           try:
               manifest = doc.package.manifest
               # In a real implementation, you'd extract and parse each content file
               # For now, return placeholder
               return "Sample text for analysis. This would contain the actual book content."
           except Exception:
               return ""
       
       def _calculate_text_stats(self, text):
           """Calculate basic text statistics."""
           # Clean text
           text = re.sub(r'[^\w\s\.\!\?]', '', text)
           
           # Count words
           words = len(text.split())
           
           # Count sentences
           sentences = len(re.findall(r'[.!?]+', text))
           if sentences == 0:
               sentences = 1  # Avoid division by zero
           
           # Count syllables (simplified)
           syllables = self._count_syllables(text)
           
           return {
               'words': words,
               'sentences': sentences,
               'syllables': syllables
           }
       
       def _count_syllables(self, text):
           """Simplified syllable counting."""
           words = text.lower().split()
           syllable_count = 0
           
           for word in words:
               word = re.sub(r'[^a-z]', '', word)
               if word:
                   # Simple syllable counting heuristic
                   vowels = 'aeiouy'
                   syllables = sum(1 for i, char in enumerate(word) 
                                 if char in vowels and (i == 0 or word[i-1] not in vowels))
                   if word.endswith('e') and syllables > 1:
                       syllables -= 1
                   syllable_count += max(1, syllables)
           
           return syllable_count
       
       def _flesch_reading_ease(self, stats):
           """Calculate Flesch Reading Ease score."""
           return (206.835 - 
                   (1.015 * (stats['words'] / stats['sentences'])) - 
                   (84.6 * (stats['syllables'] / stats['words'])))
       
       def _flesch_kincaid_grade(self, stats):
           """Calculate Flesch-Kincaid Grade Level."""
           return ((0.39 * (stats['words'] / stats['sentences'])) + 
                   (11.8 * (stats['syllables'] / stats['words'])) - 15.59)
       
       def _interpret_flesch_score(self, score):
           """Interpret Flesch Reading Ease score."""
           if score >= 90:
               return "Very Easy (5th grade)"
           elif score >= 80:
               return "Easy (6th grade)"
           elif score >= 70:
               return "Fairly Easy (7th grade)"
           elif score >= 60:
               return "Standard (8th-9th grade)"
           elif score >= 50:
               return "Fairly Difficult (10th-12th grade)"
           elif score >= 30:
               return "Difficult (College level)"
           else:
               return "Very Difficult (Graduate level)"

   # Usage
   analyzer = ReadingLevelAnalyzer()
   analysis = analyzer.analyze_epub("book.epub")

   print(f"Reading Level Analysis for: {analysis['title']}")
   print(f"Word Count: {analysis['word_count']:,}")
   print(f"Reading Level: {analysis['reading_level']}")
   print(f"Flesch-Kincaid Grade: {analysis['flesch_kincaid_grade']}")

Direct File Access and Extraction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario**: Extract specific files from EPUB archives for processing or analysis.

**CLI Approach**:

.. code-block:: bash

   #!/bin/bash
   # extract-epub-assets.sh - Extract and process EPUB content files

   epub_file="$1"
   output_dir="extracted_content"
   
   mkdir -p "$output_dir"
   
   echo "Extracting content from: $epub_file"
   
   # Get list of all XHTML content files
   epub-utils "$epub_file" files --format raw | grep '\.xhtml$' | while read -r file_path; do
       echo "Processing: $file_path"
       
       # Extract plain text content
       safe_name=$(echo "$file_path" | tr '/' '_')
       epub-utils "$epub_file" files "$file_path" --format plain > "$output_dir/${safe_name}.txt"
       
       # Extract styled HTML content
       epub-utils "$epub_file" files "$file_path" --format raw > "$output_dir/${safe_name}.html"
   done
   
   # Extract CSS files for styling reference
   epub-utils "$epub_file" files --format raw | grep '\.css$' | while read -r css_path; do
       echo "Extracting CSS: $css_path"
       safe_name=$(echo "$css_path" | tr '/' '_')
       epub-utils "$epub_file" files "$css_path" > "$output_dir/${safe_name}"
   done
   
   echo "Extraction complete! Files saved to $output_dir/"

**Comparing files vs content commands**:

.. code-block:: bash

   # Using files command (direct path access)
   epub-utils book.epub files OEBPS/chapter1.xhtml --format plain
   epub-utils book.epub files OEBPS/styles/main.css
   epub-utils book.epub files META-INF/container.xml
   
   # Using content command (requires manifest item ID)
   epub-utils book.epub manifest | grep chapter1  # Find the ID first
   epub-utils book.epub content chapter1-id --format plain

**Key advantages of the files command**:

- **Direct access**: Use actual file paths without needing manifest IDs
- **Universal file access**: Access any file type (XHTML, CSS, XML, images, etc.)
- **Simpler automation**: No need to parse manifest to find item IDs
- **Better for file-system-based workflows**: Mirrors actual EPUB structure

**Python equivalent using API**:

.. code-block:: python

   from epub_utils import Document

   def extract_file_content(epub_path, file_path):
       """Extract content from a specific file in EPUB."""
       doc = Document(epub_path)
       
       try:
           content = doc.get_file_by_path(file_path)
           
           # Handle different content types
           if hasattr(content, 'to_plain'):
               # XHTML content - can extract plain text
               return {
                   'raw_html': content.to_str(),
                   'plain_text': content.to_plain(),
                   'formatted_xml': content.to_xml(pretty_print=True)
               }
           else:
               # Other file types (CSS, XML, etc.)
               return {'raw_content': content}
               
       except ValueError as e:
           return {'error': str(e)}

   # Usage
   doc = Document("book.epub")
   
   # Extract chapter content
   chapter_content = extract_file_content("book.epub", "OEBPS/chapter1.xhtml")
   if 'plain_text' in chapter_content:
       print(f"Chapter text: {chapter_content['plain_text'][:200]}...")
   
   # Extract CSS for styling analysis
   css_content = extract_file_content("book.epub", "OEBPS/styles/main.css")
   if 'raw_content' in css_content:
       print(f"CSS rules: {len(css_content['raw_content'].split('{'))} rules found")

Automation and Workflows
-------------------------

Automated EPUB Processing Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario**: Set up an automated pipeline for processing new EPUB files.

.. code-block:: python

   import os
   import shutil
   import json
   from pathlib import Path
   from datetime import datetime
   from epub_utils import Document

   class EPUBProcessor:
       def __init__(self, input_dir, output_dir, processed_dir):
           self.input_dir = Path(input_dir)
           self.output_dir = Path(output_dir)
           self.processed_dir = Path(processed_dir)
           
           # Create directories if they don't exist
           self.output_dir.mkdir(exist_ok=True)
           self.processed_dir.mkdir(exist_ok=True)
       
       def process_new_files(self):
           """Process all new EPUB files in input directory."""
           epub_files = list(self.input_dir.glob("*.epub"))
           
           if not epub_files:
               print("No EPUB files found to process")
               return
           
           print(f"Found {len(epub_files)} EPUB files to process")
           
           results = []
           for epub_path in epub_files:
               result = self.process_single_file(epub_path)
               results.append(result)
           
           # Generate processing report
           self.generate_report(results)
           
           return results
       
       def process_single_file(self, epub_path):
           """Process a single EPUB file."""
           print(f"Processing: {epub_path.name}")
           
           try:
               doc = Document(str(epub_path))
               
               # Extract metadata
               metadata = self.extract_metadata(doc)
               
               # Validate file
               validation_result = self.validate_epub(doc)
               
               # Generate file info
               file_info = self.generate_file_info(epub_path, doc)
               
               # Create organized filename
               new_filename = self.create_organized_filename(metadata)
               
               # Move file to organized location
               organized_path = self.organize_file(epub_path, new_filename, metadata)
               
               result = {
                   'original_path': str(epub_path),
                   'new_path': str(organized_path),
                   'status': 'success',
                   'metadata': metadata,
                   'validation': validation_result,
                   'file_info': file_info,
                   'processed_at': datetime.now().isoformat()
               }
               
               # Move original to processed directory
               processed_path = self.processed_dir / epub_path.name
               shutil.move(str(epub_path), str(processed_path))
               
               return result
               
           except Exception as e:
               result = {
                   'original_path': str(epub_path),
                   'status': 'error',
                   'error': str(e),
                   'processed_at': datetime.now().isoformat()
               }
               
               # Move problematic file to processed directory
               processed_path = self.processed_dir / f"ERROR_{epub_path.name}"
               shutil.move(str(epub_path), str(processed_path))
               
               return result
       
       def extract_metadata(self, doc):
           """Extract standardized metadata."""
           metadata = doc.package.metadata
           
           return {
               'title': getattr(metadata, 'title', '').strip(),
               'author': getattr(metadata, 'creator', '').strip(),
               'publisher': getattr(metadata, 'publisher', '').strip(),
               'language': getattr(metadata, 'language', '').strip(),
               'year': self.extract_year(getattr(metadata, 'date', '')),
               'identifier': getattr(metadata, 'identifier', '').strip(),
               'subject': getattr(metadata, 'subject', '').strip()
           }
       
       def extract_year(self, date_str):
           """Extract year from date string."""
           if not date_str:
               return ''
           return date_str.split('-')[0] if '-' in date_str else date_str[:4]
       
       def validate_epub(self, doc):
           """Basic EPUB validation."""
           issues = []
           
           try:
               metadata = doc.package.metadata
               
               if not getattr(metadata, 'title', '').strip():
                   issues.append('Missing title')
               if not getattr(metadata, 'creator', '').strip():
                   issues.append('Missing author')
               if not getattr(metadata, 'language', '').strip():
                   issues.append('Missing language')
               
               # Check for content
               manifest = doc.package.manifest
               has_content = any(
                   item.get('media-type') == 'application/xhtml+xml'
                   for item in manifest.items.values()
               )
               
               if not has_content:
                   issues.append('No content files found')
               
           except Exception as e:
               issues.append(f'Validation error: {e}')
           
           return {
               'is_valid': len(issues) == 0,
               'issues': issues
           }
       
       def generate_file_info(self, epub_path, doc):
           """Generate file information."""
           stat = epub_path.stat()
           
           return {
               'filename': epub_path.name,
               'size_bytes': stat.st_size,
               'size_mb': round(stat.st_size / (1024 * 1024), 2),
               'file_count': len(doc.get_files_info()),
               'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
           }
       
       def create_organized_filename(self, metadata):
           """Create an organized filename from metadata."""
           # Clean strings for filename
           def clean_for_filename(s):
               return re.sub(r'[^\w\s-]', '', s).strip()[:50]
           
           author = clean_for_filename(metadata['author'] or 'Unknown_Author')
           title = clean_for_filename(metadata['title'] or 'Unknown_Title')
           year = metadata['year'] or 'Unknown_Year'
           
           return f"{author} - {title} ({year}).epub"
       
       def organize_file(self, epub_path, new_filename, metadata):
           """Organize file into structured directory."""
           # Create author directory
           author = metadata['author'] or 'Unknown_Author'
           author_dir = self.output_dir / author[:50]  # Limit length
           author_dir.mkdir(exist_ok=True)
           
           # Create final path
           final_path = author_dir / new_filename
           
           # Copy file to organized location
           shutil.copy2(str(epub_path), str(final_path))
           
           return final_path
       
       def generate_report(self, results):
           """Generate processing report."""
           report_path = self.output_dir / f"processing_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
           
           summary = {
               'total_files': len(results),
               'successful': len([r for r in results if r['status'] == 'success']),
               'errors': len([r for r in results if r['status'] == 'error']),
               'generated_at': datetime.now().isoformat(),
               'results': results
           }
           
           with open(report_path, 'w', encoding='utf-8') as f:
               json.dump(summary, f, indent=2, ensure_ascii=False)
           
           print(f"Processing complete!")
           print(f"Successfully processed: {summary['successful']}")
           print(f"Errors: {summary['errors']}")
           print(f"Report saved to: {report_path}")

   # Usage
   processor = EPUBProcessor(
       input_dir="/path/to/new/epubs",
       output_dir="/path/to/organized/library", 
       processed_dir="/path/to/processed/files"
   )

   results = processor.process_new_files()

Command-Line Power User Examples
--------------------------------

Advanced Shell Scripts
~~~~~~~~~~~~~~~~~~~~~~

**Complex metadata extraction with error handling**:

.. code-block:: bash

   #!/bin/bash
   # advanced-epub-analysis.sh

   set -euo pipefail

   EPUB_DIR="${1:-./}"
   OUTPUT_FILE="detailed_analysis.json"

   echo "Starting advanced EPUB analysis..."
   echo "Directory: $EPUB_DIR"
   echo "Output: $OUTPUT_FILE"

   # Initialize JSON output
   echo '{"analysis_date": "'$(date -Iseconds)'", "epubs": [' > "$OUTPUT_FILE"

   first=true
   find "$EPUB_DIR" -name "*.epub" -type f | while read -r epub; do
       echo "Analyzing: $(basename "$epub")"
       
       if [ "$first" = true ]; then
           first=false
       else
           echo "," >> "$OUTPUT_FILE"
       fi
       
       # Start JSON object for this EPUB
       echo '  {' >> "$OUTPUT_FILE"
       echo "    \"file\": \"$epub\"," >> "$OUTPUT_FILE"
       
       # Extract metadata with error handling
       if metadata=$(epub-utils "$epub" metadata --format kv 2>/dev/null); then
           echo "    \"metadata\": {" >> "$OUTPUT_FILE"
           
           # Parse metadata into JSON
           echo "$metadata" | while IFS=': ' read -r key value; do
               if [ -n "$key" ] && [ -n "$value" ]; then
                   echo "      \"$key\": \"$value\"," >> "$OUTPUT_FILE"
               fi
           done | sed '$s/,$//' # Remove last comma
           
           echo "    }," >> "$OUTPUT_FILE"
       else
           echo "    \"metadata\": null," >> "$OUTPUT_FILE"
           echo "    \"metadata_error\": true," >> "$OUTPUT_FILE"
       fi
       
       # File analysis
       if file_info=$(epub-utils "$epub" files --format raw 2>/dev/null); then
           file_count=$(echo "$file_info" | wc -l)
           echo "    \"file_count\": $file_count," >> "$OUTPUT_FILE"
       else
           echo "    \"file_count\": null," >> "$OUTPUT_FILE"
       fi
       
       # File size
       size=$(stat -f%z "$epub" 2>/dev/null || stat -c%s "$epub" 2>/dev/null || echo "0")
       echo "    \"size_bytes\": $size," >> "$OUTPUT_FILE"
       
       # Validation check
       if epub-utils "$epub" container >/dev/null 2>&1 && \
          epub-utils "$epub" package >/dev/null 2>&1; then
           echo "    \"is_valid\": true" >> "$OUTPUT_FILE"
       else
           echo "    \"is_valid\": false" >> "$OUTPUT_FILE"
       fi
       
       echo "  }" >> "$OUTPUT_FILE"
   done

   # Close JSON
   echo "]}" >> "$OUTPUT_FILE"

   echo "Analysis complete! Results in $OUTPUT_FILE"

**Batch processing with parallel execution**:

.. code-block:: bash

   #!/bin/bash
   # parallel-epub-check.sh

   EPUB_DIR="${1:-./}"
   MAX_JOBS=4

   export -f check_single_epub
   check_single_epub() {
       epub="$1"
       base=$(basename "$epub")
       
       echo "[$base] Starting check..."
       
       # Quick validation
       if ! epub-utils "$epub" container >/dev/null 2>&1; then
           echo "[$base] ❌ Invalid container"
           return 1
       fi
       
       if ! epub-utils "$epub" package >/dev/null 2>&1; then
           echo "[$base] ❌ Invalid package"
           return 1
       fi
       
       # Check for required metadata
       metadata=$(epub-utils "$epub" metadata --format kv 2>/dev/null)
       
       if ! echo "$metadata" | grep -q "^title:"; then
           echo "[$base] ⚠️  Missing title"
       fi
       
       if ! echo "$metadata" | grep -q "^creator:"; then
           echo "[$base] ⚠️  Missing author"
       fi
       
       echo "[$base] ✅ Check complete"
   }

   # Run parallel checks
   find "$EPUB_DIR" -name "*.epub" -type f | \
   xargs -n 1 -P $MAX_JOBS -I {} bash -c 'check_single_epub "$@"' _ {}

These examples demonstrate the power and flexibility of ``epub-utils`` for various real-world scenarios. Whether you're managing a digital library, performing quality assurance, or building automated workflows, epub-utils provides the tools you need to work effectively with EPUB files.
