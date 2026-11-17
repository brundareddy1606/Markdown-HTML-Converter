import re
import argparse
import html
import sys
from pathlib import Path


# ==========================================
# MARKDOWN TO HTML CONVERTER
# CodeNova Python Internship - Task 3
# ==========================================


class MarkdownConverter:

    def __init__(self):
        self.css = """
        body {
            font-family: Arial, Helvetica, sans-serif;
            background: #f4f6f9;
            color: #333;
            line-height: 1.8;
            max-width: 900px;
            margin: 40px auto;
            padding: 30px;
        }

        main {
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }

        h1, h2, h3, h4 {
            color: #243b64;
            margin-top: 25px;
        }

        h1 {
            border-bottom: 3px solid #4a90e2;
            padding-bottom: 10px;
        }

        a {
            color: #1673c9;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        ul, ol {
            padding-left: 30px;
        }

        li {
            margin: 5px 0;
        }

        code {
            background: #eef1f5;
            padding: 3px 6px;
            border-radius: 4px;
        }

        p {
            margin: 15px 0;
        }

        @media (max-width: 600px) {
            body {
                margin: 10px;
                padding: 10px;
            }

            main {
                padding: 20px;
            }
        }
        """

    # Convert bold, italic and hyperlinks
    def convert_inline(self, text):

        text = html.escape(text, quote=False)

        # Convert links and validate their URL schemes
        link_pattern = r'\[([^\]]+)\]\(([^)\s]+)\)'

        def replace_link(match):
            label = match.group(1)
            url = html.unescape(match.group(2))

            if not re.match(
                r'^(https?://|mailto:|/|#)',
                url,
                re.IGNORECASE
            ):
                return label

            safe_url = html.escape(url, quote=True)

            return (
                f'<a href="{safe_url}" '
                f'target="_blank" rel="noopener noreferrer">'
                f'{label}</a>'
            )

        text = re.sub(link_pattern, replace_link, text)

        # Convert bold text
        text = re.sub(
            r'\*\*(.+?)\*\*',
            r'<strong>\1</strong>',
            text
        )

        text = re.sub(
            r'__(.+?)__',
            r'<strong>\1</strong>',
            text
        )

        # Convert italic text
        text = re.sub(
            r'(?<!\*)\*([^*\n]+)\*(?!\*)',
            r'<em>\1</em>',
            text
        )

        text = re.sub(
            r'(?<!_)_([^_\n]+)_(?!_)',
            r'<em>\1</em>',
            text
        )

        return text

    # Convert Markdown headings
    def convert_heading(self, line):

        match = re.match(r'^(#{1,4})\s+(.+?)\s*#*\s*$', line)

        if match:
            level = len(match.group(1))
            content = self.convert_inline(match.group(2))

            return f'<h{level}>{content}</h{level}>'

        return None

    # Convert Markdown lists
    def convert_lists(self, lines):

        result = []
        stack = []

        list_pattern = r'^(\s*)([-*+]|\d+[.)])\s+(.+)$'

        def close_lists():
            while stack:
                item = stack.pop()

                if item["li_open"]:
                    result.append("</li>")

                result.append(f'</{item["tag"]}>')

        for line in lines:

            match = re.match(list_pattern, line)

            if not match:
                close_lists()
                result.append(line)
                continue

            indentation = len(match.group(1).expandtabs(4))
            marker = match.group(2)
            content = self.convert_inline(match.group(3))

            tag = "ul" if marker in ("-", "*", "+") else "ol"

            # Close deeper lists when indentation decreases
            while stack and indentation < stack[-1]["indent"]:
                close_item = stack.pop()

                if close_item["li_open"]:
                    result.append("</li>")

                result.append(f'</{close_item["tag"]}>')

            if stack and indentation == stack[-1]["indent"]:

                # Continue an existing list
                if stack[-1]["tag"] == tag:

                    if stack[-1]["li_open"]:
                        result.append("</li>")

                else:
                    # Switch between ordered and unordered lists
                    close_item = stack.pop()

                    if close_item["li_open"]:
                        result.append("</li>")

                    result.append(f'</{close_item["tag"]}>')

                    result.append(f'<{tag}>')

                    stack.append({
                        "indent": indentation,
                        "tag": tag,
                        "li_open": False
                    })

            elif not stack or indentation > stack[-1]["indent"]:

                # Open a new list, including nested lists
                result.append(f'<{tag}>')

                stack.append({
                    "indent": indentation,
                    "tag": tag,
                    "li_open": False
                })

            result.append(f'<li>{content}>'.replace(
                f'{content}>', content
            ))

            stack[-1]["li_open"] = True

        close_lists()

        return "\n".join(result)

    # Convert complete Markdown document
    def convert_markdown(self, markdown_text):

        lines = markdown_text.splitlines()
        processed = self.convert_lists(lines)

        lines = processed.splitlines()

        output = []
        paragraph = []

        def flush_paragraph():

            if paragraph:
                content = " ".join(paragraph)
                output.append(
                    f'<p>{self.convert_inline(content)}</p>'
                )
                paragraph.clear()

        for line in lines:

            stripped = line.strip()

            if not stripped:
                flush_paragraph()
                continue

            heading = self.convert_heading(stripped)

            if heading:
                flush_paragraph()
                output.append(heading)

            elif stripped.startswith(("<ul>", "<ol>", "</ul>", "</ol>", "<li>", "</li>")):
                flush_paragraph()
                output.append(stripped)

            else:
                paragraph.append(stripped)

        flush_paragraph()

        return "\n".join(output)

    # Create complete HTML5 document
    def create_html(self, markdown_text):

        body = self.convert_markdown(markdown_text)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Converted Markdown document">
    <title>Markdown to HTML Converter</title>
    <style>
{self.css}
    </style>
</head>
<body>
    <main>
{body}
    </main>
</body>
</html>
"""

    # Read Markdown and save HTML
    def convert_file(self, input_path, output_path):

        source = Path(input_path)
        destination = Path(output_path)

        if not source.exists():
            raise FileNotFoundError(
                f"Input file not found: {source}"
            )

        if not source.is_file():
            raise ValueError("Input path is not a file.")

        markdown_text = source.read_text(encoding="utf-8")

        if not markdown_text.strip():
            raise ValueError("Input Markdown file is empty.")

        html_document = self.create_html(markdown_text)

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        destination.write_text(
            html_document,
            encoding="utf-8"
        )

        return destination


# ==========================================
# COMMAND LINE INTERFACE
# ==========================================

def main():

    parser = argparse.ArgumentParser(
        description="Convert Markdown files into styled HTML documents."
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to the source Markdown file."
    )

    parser.add_argument(
        "-o", "--output",
        help="Path for the generated HTML file."
    )

    args = parser.parse_args()

    input_path = Path(args.input)

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix(".html")

    converter = MarkdownConverter()

    try:

        result = converter.convert_file(
            input_path,
            output_path
        )

        print("\n================================")
        print(" MARKDOWN TO HTML CONVERTER")
        print("================================")
        print("Conversion successful!")
        print(f"Input file : {input_path}")
        print(f"Output file: {result}")
        print("================================\n")

    except FileNotFoundError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)

    except PermissionError:
        print(
            "ERROR: Permission denied. Check file permissions.",
            file=sys.stderr
        )
        sys.exit(1)

    except (ValueError, UnicodeError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()