import os
import json
import sqlite3
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import atexit
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings, HuggingFaceInferenceAPIEmbeddings

app = Flask(__name__)
CORS(app)

# Load API keys
with open("api_key.json", "r") as api_file:
    api = json.load(api_file)
HUGGINGFACE_API_KEY = api["HUGGINGFACE_API_KEY"]
XAI_API_KEY = api["XAI_API_KEY"]

if HUGGINGFACE_API_KEY:
    embedding_function = HuggingFaceInferenceAPIEmbeddings(
        api_key=HUGGINGFACE_API_KEY,
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
else:
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize ChromaDB
vector_store = Chroma(persist_directory="../chroma_db", embedding_function=embedding_function)
retriever = vector_store.as_retriever()

DB_CONNECTION = "chat_history.db"  # SQLite file for local use

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_CONNECTION)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_query TEXT,
            assistant_response TEXT
        );
    ''')
    conn.commit()
    conn.close()

init_db()

# Store chat history in database
def get_chat_history():
    try:
        conn = sqlite3.connect(DB_CONNECTION)
        c = conn.cursor()
        c.execute("SELECT user_query, assistant_response FROM chats ORDER BY id DESC LIMIT 10")
        chat_history = [[{"role": "user", "content": row[0]}, {"role": "assistant", "content": row[1]}] for row in reversed(c.fetchall())]
        conn.close()
        return chat_history
    except Exception as e:
        return []

def update_chat_history(user_query, response):
    try:
        conn = sqlite3.connect(DB_CONNECTION)
        c = conn.cursor()
        c.execute("INSERT INTO chats (user_query, assistant_response) VALUES (?, ?)", (user_query, response))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error updating chat history: {e}")
        
def clear_chat_history(exception=None):
    try:
        conn = sqlite3.connect(DB_CONNECTION)
        c = conn.cursor()
        c.execute("DELETE FROM chats;")  # Delete all records
        conn.commit()
        conn.close()
        print("Chat history cleared")
    except Exception as e:
        print(f"Error clearing chat history: {e}")

# Function to get response from AI
def chat_with_ai(query):
    try:    
        url = "https://api.x.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {XAI_API_KEY}",
            "Content-Type": "application/json",
        }
        response = requests.post(
            url=url,
            headers=headers,
            json={"messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": query}
                    ], 
                "model": "grok-2-latest",
                    "stream": False,
                    "temperature": 0.7  }
        )
        response_json = response.json()
        if "choices" in response_json and response_json["choices"]:
            return response_json["choices"][0]["message"]["content"]
        else:
            return "Error: No valid response from AI."
    except Exception as e:
        return f"Error processing request: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"response": "Please provide a query."})

    #getting chat history
    chat_history = get_chat_history()

    # Retrieve relevant context
    retrieved_docs = retriever.get_relevant_documents(user_query)
    retrieved_text = "\n".join([doc.page_content for doc in retrieved_docs])
    
        # Combine retrieved knowledge with the query and chat history
    full_query = f'''Chat history:\n {chat_history}\n
    \nUse the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
\n{retrieved_text}\n\n Note 1: If the context provided does not contain information relevant to the question, then reply as a normal chatbot.\n
Note 2: If the context provided contains information relevant to the question, then reply as a first person based on the context.\n
Note 3: When answering the question, make sure to provide a clear and concise response. And do not say that you are replying based on context.\n
Note 4: Properly format your response to the question.\n
\n\nQuestion: {user_query}'''

    # Get response from Grok AI
    response = chat_with_ai(full_query)

    # Update chat history
    update_chat_history(user_query, response)

    return jsonify({"response": response})
        
@app.route("/clearchat", methods=["POST"])
def clear_chat():
    clear_chat_history()
    return jsonify({"response": "Chat history cleared."})

atexit.register(clear_chat_history)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
