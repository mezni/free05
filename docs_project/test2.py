from docling.document_converter import DocumentConverter
import docx

def process_word_to_json(file_path):
    # 1. Extract Core Metadata using python-docx
    doc = docx.Document(file_path)
    props = doc.core_properties
    metadata = {
        "title": props.title,
        "author": props.author,
        "last_modified_by": props.last_modified_by,
        "created": str(props.created),
        "source": file_path
    }

    # 2. Convert Content to Structured JSON using Docling
    converter = DocumentConverter()
    result = converter.convert(file_path)
    
    # Export to a structured dictionary (includes headings, tables, etc.)
    content_json = result.document.export_to_dict()
    
    return {"metadata": metadata, "content": content_json}

file_path="test.docx"
process_word_to_json(file_path)
