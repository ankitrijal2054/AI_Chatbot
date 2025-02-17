import streamlit as st
from chatbot import chat_with_ai

# Streamlit page configuration
st.set_page_config(page_title="Ankit's AI Chatbot", layout="wide")

# Title
st.title("🤖 Chat with Ankit's AI Assistant")
st.write("Ask me anything about Ankit's career, skills, and personal life!")

# User input field
user_query = st.text_input("Type your question here:")

# Process user query
if user_query:
    response = chat_with_ai(user_query)
    st.write("**AI Response:**")
    st.write(response)

