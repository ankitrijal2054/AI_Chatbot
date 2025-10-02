import os
import json
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import atexit
from cartesia import Cartesia
from concurrent.futures import ThreadPoolExecutor

# ✅ Updated imports
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from google import genai  # new Google GenAI SDK

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# Load API keys
with open("api_key.json", "r") as api_file:
    api = json.load(api_file)

HF_TOKEN = api.get("HF_TOKEN")
GOOGLE_API_KEY = api.get("GOOGLE_API_KEY")
CARTESIA_API_KEY = api.get("CARTESIA_API_KEY")

# ✅ Configure Google Gemini client
client = genai.Client(api_key=GOOGLE_API_KEY)

# ✅ Use local embeddings for now
print("💻 Using local Hugging Face embeddings...")
embedding_function = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ✅ Chroma vector store
vector_store = Chroma(
    persist_directory="../chroma_db",
    embedding_function=embedding_function
)
retriever = vector_store.as_retriever()

DB_CONNECTION = "chat_history.db"  # SQLite file for local use

# ---------- Database Setup ----------
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

def get_chat_history():
    """Retrieve last 10 chats from DB"""
    try:
        with sqlite3.connect(DB_CONNECTION) as conn:
            c = conn.cursor()
            c.execute("SELECT user_query, assistant_response FROM chats ORDER BY id DESC LIMIT 10")
            rows = c.fetchall()
        return [[{"role": "user", "content": row[0]}, {"role": "assistant", "content": row[1]}] for row in reversed(rows)]
    except Exception as e:
        print(f"Error retrieving chat history: {e}")
        return []

def update_chat_history(user_query, response):
    """Insert a new chat into DB"""
    try:
        with sqlite3.connect(DB_CONNECTION) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO chats (user_query, assistant_response) VALUES (?, ?)", (user_query, response))
            conn.commit()
    except Exception as e:
        print(f"Error updating chat history: {e}")

def clear_chat_history(exception=None):
    """Clear DB on shutdown or /clearchat call"""
    try:
        with sqlite3.connect(DB_CONNECTION) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM chats;")
            conn.commit()
        print("Chat history cleared")
    except Exception as e:
        print(f"Error clearing chat history: {e}")

# ---------- AI Chat ----------
def chat_with_ai(query: str) -> str:
    print("Sending query to Google Gemini (new SDK)...")
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",  # or gemini-1.5-pro if flash not supported
            contents=query,
        )
        return response.text
    except Exception as e:
        return f"Error processing request: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"response": "Please provide a query."})

    # Retrieve chat history + docs concurrently
    with ThreadPoolExecutor() as executor:
        future_history = executor.submit(get_chat_history)
        future_docs = executor.submit(retriever.invoke, user_query)

        chat_history = future_history.result()
        retrieved_docs = future_docs.result()

    retrieved_text = "\n".join([doc.page_content for doc in retrieved_docs])

    full_query = f"""Chat history:
{chat_history}

Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know.
{retrieved_text}

Notes:
1. If context is irrelevant → answer normally as a chatbot.
2. If relevant → answer in first person as if it's your own knowledge.
3. Always be clear and concise, don't mention the context directly.
4. Properly format your response.

Question: {user_query}"""

    response = chat_with_ai(full_query)
    update_chat_history(user_query, response)

    return jsonify({"response": response})

@app.route("/clearchat", methods=["POST"])
def clear_chat():
    clear_chat_history()
    return jsonify({"response": "Chat history cleared."})

# ---------- TTS ----------
@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    transcript = data.get("text", "")
    if not transcript:
        return jsonify({"error": "No text provided."}), 400

    try:
        if CARTESIA_API_KEY is None:
            raise ValueError("CARTESIA_API_KEY is not set")
        client_tts = Cartesia(api_key=CARTESIA_API_KEY)
        audio_bytes = client_tts.tts.bytes(
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

# ---------- Cleanup ----------
atexit.register(clear_chat_history)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
