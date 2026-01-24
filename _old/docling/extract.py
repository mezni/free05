from docling.document_converter import DocumentConverter
from docling_core.transforms.chunker import HybridChunker

# 1. Initialize the converter
converter = DocumentConverter()

# 2. Convert the DOCX file (replace with your actual file path)
source = "../recouvrement.docx"
result = converter.convert(source)

json_output = result.document.export_to_dict()

# 3. Access the converted content (e.g., as Markdown)
print(result.document.export_to_markdown())


print (json_output)



chunker = HybridChunker()

# 3. Generate chunks
chunk_iter = chunker.chunk(result.document)

# 4. Process the chunks
for chunk in chunk_iter:
    print(f"--- Chunk (Page {chunk.meta.doc_items[0].prov[0].page_no}) ---")
    print(chunk.text)