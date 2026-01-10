from haystack import Pipeline
from haystack.components.converters.docx import DOCXToDocument
from haystack.components.preprocessors import DocumentSplitter
from haystack.dataclasses import ByteStream

# 1. Initialize Components
# table_format="markdown" ensures tables are readable in the output JSON
converter = DOCXToDocument(table_format="markdown") 
splitter = DocumentSplitter(split_by="passage", split_length=1) # "passage" splits by double newlines (paragraphs/sections)

# 2. Build Pipeline
indexing_pipeline = Pipeline()
indexing_pipeline.add_component("converter", converter)
indexing_pipeline.add_component("splitter", splitter)
indexing_pipeline.connect("converter", "splitter")

# 3. Run Pipeline
results = indexing_pipeline.run({
    "converter": {"sources": ["test.docx"]}
})

# The "nodes" are now in results["splitter"]["documents"]
documents = results["splitter"]["documents"]

import json

json_output = []
for doc in documents:
    json_output.append({
        "content": doc.content,
        "metadata": doc.meta, # Contains filename, etc.
        "id": doc.id
    })

with open("haystack_output.json", "w") as f:
    json.dump(json_output, f, indent=4)