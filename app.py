import streamlit as st
from chatbot import chat_with_ai

st.set_page_config(page_title="Ankit's AI Chatbot", layout="wide")

st.title("🤖 Chat with Ankit's AI Assistant")
st.write("Ask me anything about Ankit's career, skills, and personal life!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Button to clear chat history
if st.button("🗑️ New Chat"):
    st.session_state.messages = []  
    st.rerun() 

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input field
user_query = st.chat_input("Type your question here...")

# Process user query and update chat history
if user_query:
    # Display user's message
    with st.chat_message("user"):
        st.write(user_query)

    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Get AI response
    response = chat_with_ai(user_query)

    # Display AI response
    with st.chat_message("assistant"):
        st.write(response)

    # Append AI response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})
