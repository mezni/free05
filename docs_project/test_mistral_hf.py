from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

# Load pre-trained model and tokenizer
model_name = "mistralai/Mistral-7B-Instruct-v0.2"
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Create a question answering pipeline
qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)

# Test it out!
context = "Mistral is a French word meaning 'a strong, cold, northwesterly wind that blows from southern France into the Gulf of Lion in the northern Mediterranean.'"
question = "What does Mistral mean?"

result = qa_pipeline(question=question, context=context)
print(result)