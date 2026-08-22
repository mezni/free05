import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


# Load environment variables from .env
load_dotenv()

# Read environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")


# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------

st.title("LangChain Chatbot")

# Get the user's question
input_text = st.text_input(
    "Ask a question",
    placeholder="Enter your question..."
)


# --------------------------------------------------
# LangChain Prompt
# --------------------------------------------------

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. "
            "Please respond to the user's queries."
        ),
        (
            "user",
            "Question: {question}"
        ),
    ]
)


# --------------------------------------------------
# Language Model
# --------------------------------------------------

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
)


# --------------------------------------------------
# Output Parser
# --------------------------------------------------

output_parser = StrOutputParser()


# --------------------------------------------------
# Create LangChain Chain
# --------------------------------------------------

chain = prompt | llm | output_parser


# --------------------------------------------------
# Execute Chain
# --------------------------------------------------

if input_text:
    response = chain.invoke(
        {
            "question": input_text,
        }
    )

    st.write(response)