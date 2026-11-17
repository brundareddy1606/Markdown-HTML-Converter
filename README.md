Markdown to HTML Static Document Converter

Project Overview

The Markdown to HTML Static Document Converter is a Python-based application that converts Markdown (".md") files into professionally styled HTML5 documents.

It uses regular expressions and Python file-handling modules to process Markdown elements and generate standalone HTML pages with embedded CSS.

Features

- Converts H1, H2, H3 and H4 headings.
- Supports bold and italic formatting.
- Converts bulleted and numbered lists.
- Supports nested lists.
- Converts hyperlinks.
- Generates standalone HTML5 documents.
- Includes modern embedded CSS styling.
- Supports custom input and output file paths.
- Handles missing and empty input files.
- Handles permission and file errors.
- Supports UTF-8 text.

Technologies Used

- Python 3
- Regular Expressions ("re")
- HTML
- CSS
- "argparse"
- "pathlib"
- "html"
- "sys"

Project Structure

Markdown_HTML_Converter/
│
├── converter.py
├── sample.md
├── README.md
│
└── output/
    └── sample.html

Requirements

- Python 3.x
- Visual Studio Code (recommended)

No external Python packages are required.

Installation

1. Download or clone the project.
2. Open the project folder in VS Code.
3. Open the integrated terminal.
4. Run the converter using the commands below.

How to Run

Basic conversion

python converter.py -i sample.md

Specify output location

python converter.py -i sample.md -o output/sample.html

Display help

python converter.py --help

Supported Markdown Syntax

Markdown| HTML
"# Heading"| H1
"## Heading"| H2
"### Heading"| H3
"#### Heading"| H4
"**Bold**"| Strong
"*Italic*"| Emphasis
"- Item"| Unordered list
"1. Item"| Ordered list
"[Google](https://google.com)"| Hyperlink

Error Handling

The application handles:

- Missing input files.
- Empty Markdown documents.
- Invalid input paths.
- Permission errors.
- File reading and writing errors.

Output

The converted HTML document is saved at the specified destination and can be opened in any standard web browser.

Author

Python Programming Internship – CodeNova Batch 02

License

This project was developed as an educational internship project.