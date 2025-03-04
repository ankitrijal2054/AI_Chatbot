import os
import json
import sqlite3
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import atexit
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings, HuggingFaceInferenceAPIEmbeddings
from cartesia import Cartesia  # Import Cartesia for TTS
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
CORS(app)

# Load API keys
with open("api_key.json", "r") as api_file:
    api = json.load(api_file)
HUGGINGFACE_API_KEY = api["HUGGINGFACE_API_KEY"]
XAI_API_KEY = api["XAI_API_KEY"]
CARTESIA_API_KEY = api["CARTESIA_API_KEY"]

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
    with sqlite3.connect(DB_CONNECTION) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_query TEXT,
                assistant_response TEXT
            );
        ''')
        conn.commit()

init_db()

# Store chat history in database
def get_chat_history():
    try:
        with sqlite3.connect(DB_CONNECTION) as conn:
            c = conn.cursor()
            c.execute("SELECT user_query, assistant_response FROM chats ORDER BY id DESC LIMIT 10")
            rows = c.fetchall()
        chat_history = [[{"role": "user", "content": row[0]}, {"role": "assistant", "content": row[1]}] for row in reversed(rows)]
        return chat_history
    except Exception as e:
        print(f"Error retrieving chat history: {e}")
        return []

def update_chat_history(user_query, response):
    try:
        with sqlite3.connect(DB_CONNECTION) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO chats (user_query, assistant_response) VALUES (?, ?)", (user_query, response))
            conn.commit()
    except Exception as e:
        print(f"Error updating chat history: {e}")
        
def clear_chat_history(exception=None):
    try:
        with sqlite3.connect(DB_CONNECTION) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM chats;")
            conn.commit()
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
            json={
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": query}
                ],
                "model": "grok-2-latest",
                "stream": False,
                "temperature": 0.7  
            }
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

    # Run retrieval of chat history and documents concurrently
    with ThreadPoolExecutor() as executor:
        future_history = executor.submit(get_chat_history)
        future_docs = executor.submit(retriever.get_relevant_documents, user_query)
        chat_history = future_history.result()
        retrieved_docs = future_docs.result()

    retrieved_text = "\n".join([doc.page_content for doc in retrieved_docs])
    
    full_query = f"""Chat history:
{chat_history}

Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
{retrieved_text}

Note 1: If the context provided does not contain information relevant to the question, then reply as a normal chatbot.
Note 2: If the context provided contains information relevant to the question, then reply as a first person based on the context.
Note 3: When answering the question, make sure to provide a clear and concise response. And do not say that you are replying based on context.
Note 4: Properly format your response to the question.

Question: {user_query}"""

    response = chat_with_ai(full_query)
    update_chat_history(user_query, response)

    return jsonify({"response": response})

@app.route("/clearchat", methods=["POST"])
def clear_chat():
    clear_chat_history()
    return jsonify({"response": "Chat history cleared."})

# New TTS endpoint using Cartesia API for high-quality voice output
@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    transcript = data.get("text", "")
    if not transcript:
        return jsonify({"error": "No text provided."}), 400

    try:
        if CARTESIA_API_KEY is None:
            raise ValueError("CARTESIA_API_KEY is not set")
        client = Cartesia(api_key=CARTESIA_API_KEY)
        audio_bytes = client.tts.bytes(
            model_id="sonic",
            transcript=transcript,
            voice_id="b9022c72-058c-4e6e-93c2-e7721aae9d59",
            output_format={
                "container": "wav",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            },
        )
        return app.response_class(
            response=audio_bytes,
            status=200,
            mimetype="audio/wav"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

atexit.register(clear_chat_history)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
