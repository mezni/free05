from pathlib import Path
from docling.document_converter import DocumentConverter

# 1. Initialize and Convert
converter = DocumentConverter()
source = "../../DATA/P250U_APV_1.3_2026-01-21.docx"
result = converter.convert(source)

# 2. Export to Markdown string
document = result.document
markdown_output = document.export_to_markdown()

# 3. Define the output path
# This saves it in the same directory as your script with a .md extension
output_path = Path("output_document.md")

# 4. Write to file
with output_path.open("w", encoding="utf-8") as f:
    f.write(markdown_output)

print(f"Markdown successfully saved to {output_path}")