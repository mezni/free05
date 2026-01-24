from pathlib import Path
from docling.document_converter import DocumentConverter
from transformers import pipeline
from PIL import Image

# 1. SETUP: Docling & Hugging Face Models
converter = DocumentConverter()
# Free text summarizer (BART)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
# Free vision model for image descriptions (Salesforce BLIP is fast & free)
image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

# 2. PARSE: Convert Document
source = "../../DATA/P250U_APV_1.3_2026-01-21.docx"
result = converter.convert(source)
doc = result.document

# 3. EXTRACT: Gather text and describe images
document_content = []

for element, _level in doc.iterate_items():
    # If it's text or a table (Docling includes tables in iterate_items)
    if element.label in ["paragraph", "heading", "table"]:
        document_content.append(element.text)
    
    # If it's an image, generate a caption to "include" it in the summary
    elif element.label == "picture":
        # Note: element.get_image(doc) returns a PIL image object
        img = element.get_image(doc)
        if img:
            caption = image_to_text(img)[0]['generated_text']
            document_content.append(f"[Image Description: {caption}]")

# 4. SUMMARIZE: Combine and process
full_text = "\n".join(document_content)

# Handle potential length issues by taking the first 1024 tokens (~800 words)
# For very long docs, use the chunking method from the previous step
summary = summarizer(full_text[:3000], max_length=150, min_length=50, do_sample=False)

print("\n--- DOCUMENT SUMMARY ---\n")
print(summary[0]['summary_text'])