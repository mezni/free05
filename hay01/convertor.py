from haystack import Pipeline
from haystack.components.converters.docx import DOCXToDocument
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack_integrations.document_stores.chroma import ChromaDocumentStore


from haystack import component, Document
from typing import List

@component
class MetadataCleaner:
    @component.output_types(documents=List[Document])
    def run(self, documents: List[Document]):
        for doc in documents:
            # Create a copy of keys to avoid 'dict size changed during iteration'
            keys_to_fix = list(doc.meta.keys())
            for key in keys_to_fix:
                val = doc.meta[key]
                # If the value is not a supported type, convert to string or delete
                if not isinstance(val, (str, int, float, bool)):
                    # Option A: Convert to string so you don't lose the data
                    doc.meta[key] = str(val) 
                    # Option B: Or delete it if it's junk: del doc.meta[key]
        return {"documents": documents}

# 1. Setup Store
document_store = ChromaDocumentStore(persist_path="chroma_db")

# 2. Initialize Components
converter = DOCXToDocument(table_format="markdown")
splitter = DocumentSplitter(split_by="passage", split_length=1)
cleaner = MetadataCleaner() # Our new custom component
writer = DocumentWriter(document_store=document_store)

# 3. Build Pipeline
indexing_pipeline = Pipeline()
indexing_pipeline.add_component("converter", converter)
indexing_pipeline.add_component("splitter", splitter)
indexing_pipeline.add_component("cleaner", cleaner)
indexing_pipeline.add_component("writer", writer)

# 4. Connect Flow
indexing_pipeline.connect("converter", "splitter")
indexing_pipeline.connect("splitter", "cleaner")
indexing_pipeline.connect("cleaner", "writer")

# 5. Run
indexing_pipeline.run({"converter": {"sources": ["test.docx"]}})


from haystack_integrations.components.retrievers.chroma import ChromaQueryTextRetriever

query_pipeline = Pipeline()
query_pipeline.add_component("retriever", ChromaQueryTextRetriever(document_store))

query = "What are the key findings in the table?"
results = query_pipeline.run({"retriever": {"query": query, "top_k": 2}})

for doc in results["retriever"]["documents"]:
    print(f"Node Content: {doc.content}\n---")