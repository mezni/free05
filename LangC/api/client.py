import requests
import streamlit as st


def get_response_model1(topic: str):
    response = requests.post(
        "http://localhost:8000/en/invoke",
        json={
            "input": {
                "topic": topic,
            }
        },
    )

    response.raise_for_status()

    return response.json()["output"]["content"]


def get_response_model2(topic: str):
    response = requests.post(
        "http://localhost:8000/fr/invoke",
        json={
            "input": {
                "topic": topic,
            }
        },
    )

    response.raise_for_status()

    return response.json()["output"]["content"]


# Streamlit UI
st.title("LangChain Name Generator")

topic = st.text_input("Enter a topic")

if topic:
    english_response = get_response_model1(topic)
    french_response = get_response_model2(topic)

    st.subheader("English Names")
    st.write(english_response)

    st.subheader("French Names")
    st.write(french_response)