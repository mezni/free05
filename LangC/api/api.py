import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langserve import add_routes


# Load environment variables from .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Create FastAPI application
app = FastAPI(
    title="LangChain API",
    version="1.0",
    description="LangChain API",
)


# English prompt
prompt1 = ChatPromptTemplate.from_template(
    "Generate 5 names in English: {topic}"
)


# French prompt
prompt2 = ChatPromptTemplate.from_template(
    "Generate 5 names in French: {topic}"
)


# Create language models
model1 = ChatOpenAI(model="gpt-4o-mini")
model2 = ChatOpenAI(model="gpt-4o-mini")


# Create LangChain chains
chain1 = prompt1 | model1
chain2 = prompt2 | model2


# English API endpoint
add_routes(
    app,
    chain1,
    path="/en",
)


# French API endpoint
add_routes(
    app,
    chain2,
    path="/fr",
)


# Start server
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )