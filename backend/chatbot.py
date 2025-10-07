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

# =========================================
# Flask App Setup
# =========================================
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# =========================================
# Load API Keys
# =========================================
with open("api_key.json", "r") as api_file:
    api = json.load(api_file)

HF_TOKEN = api.get("HF_TOKEN")
GOOGLE_API_KEY = api.get("GOOGLE_API_KEY")
CARTESIA_API_KEY = api.get("CARTESIA_API_KEY")

# =========================================
# Google Gemini Client
# =========================================
client = genai.Client(api_key=GOOGLE_API_KEY)

# =========================================
# Embeddings (local)
# =========================================
print("💻 Using local Hugging Face embeddings...")
embedding_function = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =========================================
# Vector Store
# =========================================
vector_store = Chroma(
    collection_name="ankit_rijal_kb",          # must match add_knowledge.py
    persist_directory="../chroma_db",          # auto-loads persisted DB
    embedding_function=embedding_function,
)

# Retrieve top 5 most relevant documents
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# =========================================
# Database Setup (chat history)
# =========================================
DB_CONNECTION = "chat_history.db"

def init_db():
    with sqlite3.connect(DB_CONNECTION) as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_query TEXT,
                assistant_response TEXT
            );
            """
        )
        conn.commit()

init_db()

def get_chat_history():
    """Retrieve last 10 chats from DB"""
    try:
        with sqlite3.connect(DB_CONNECTION) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT user_query, assistant_response FROM chats ORDER BY id DESC LIMIT 10"
            )
            rows = c.fetchall()
        return [
            [
                {"role": "user", "content": row[0]},
                {"role": "assistant", "content": row[1]},
            ]
            for row in reversed(rows)
        ]
    except Exception as e:
        print(f"⚠️ Error retrieving chat history: {e}")
        return []

def update_chat_history(user_query, response):
    """Insert a new chat into DB"""
    try:
        with sqlite3.connect(DB_CONNECTION) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO chats (user_query, assistant_response) VALUES (?, ?)",
                (user_query, response),
            )
            conn.commit()
    except Exception as e:
        print(f"⚠️ Error updating chat history: {e}")

def clear_chat_history(exception=None):
    """Clear DB on shutdown or /clearchat call"""
    try:
        with sqlite3.connect(DB_CONNECTION) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM chats;")
            conn.commit()
        print("🧹 Chat history cleared")
    except Exception as e:
        print(f"⚠️ Error clearing chat history: {e}")

# =========================================
# AI Chat Function
# =========================================
def chat_with_ai(query: str) -> str:
    print("🚀 Sending query to Google Gemini (new SDK)...")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=query,
        )
        return response.text
    except Exception as e:
        return f"Error processing request: {str(e)}"

# =========================================
# Routes
# =========================================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_query = data.get("query", "").strip()

    if not user_query:
        return jsonify({"response": "Please provide a query."})

    # Retrieve chat history + docs concurrently
    with ThreadPoolExecutor() as executor:
        future_history = executor.submit(get_chat_history)
        future_docs = executor.submit(retriever.get_relevant_documents, user_query)

        chat_history = future_history.result()
        try:
            retrieved_docs = future_docs.result()
        except Exception as e:
            print(f"⚠️ Retrieval error: {e}")
            retrieved_docs = []

    # Combine retrieved context into structured text
    retrieved_text = "\n\n".join(
        [
            f"From {doc.metadata.get('section', 'Unknown Section')}:\n{doc.page_content}"
            for doc in retrieved_docs
        ]
    )

    # Compose final query for Gemini
    full_query = f"""
        You are Ankit Rijal's personal assistant chatbot. 
        Your job is to answer user questions about Ankit clearly, concisely, and in first person (as if you are Ankit). 

        Guidelines:
        1. **Answer Style**:
        - Default: Keep responses short, crisp, and conversational (2–4 sentences).
        - If the user asks for details, examples, or "explain more" → provide a longer, structured answer.
        - Never give long generic explanations unless explicitly requested.
        - If unsure, say "I don’t know" instead of making things up.

        2. **Context Usage**:
        - Use the retrieved knowledge base context below if it is relevant.
        - Do not mention "retrieved documents" or "context."
        - If irrelevant, just answer normally.

        3. **Tone**:
        - Friendly, professional, first person.
        - Speak naturally, like a human conversation.
        - No filler or rambling.

        ---

        ### Recent Chat History:
        {chat_history}

        ### Knowledge Base Context:
        {retrieved_text}

        ---

        ### User Question:
        {user_query}

"""


    print("🧠 Final query sent to model:\n", full_query[:1000], "...\n")

    # Send to Gemini and store chat
    response = chat_with_ai(full_query)
    update_chat_history(user_query, response)

    return jsonify({"response": response})

@app.route("/clearchat", methods=["POST"])
def clear_chat():
    clear_chat_history()
    return jsonify({"response": "Chat history cleared."})

# =========================================
# TTS Endpoint
# =========================================
@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    transcript = data.get("text", "")
    if not transcript:
        return jsonify({"error": "No text provided."}), 400

    try:
        if not CARTESIA_API_KEY:
            print("❌ CARTESIA_API_KEY is not set")
            raise ValueError("CARTESIA_API_KEY is not set")

        print(f"🎤 Generating speech for: {transcript[:50]}...")
        client_tts = Cartesia(api_key=CARTESIA_API_KEY)
        audio_generator = client_tts.tts.bytes(
            model_id="sonic-english",
            transcript=transcript,
            voice={
                "mode": "id",
                "id": "b9022c72-058c-4e6e-93c2-e7721aae9d59"
            },
            output_format={
                "container": "wav",
                "encoding": "pcm_s16le",
                "sample_rate": 24000,
            },
        )
        
        # Convert generator to bytes
        audio_bytes = b"".join(audio_generator)

        print(f"✅ Generated {len(audio_bytes)} bytes of audio")
        return app.response_class(
            response=audio_bytes,
            status=200,
            mimetype="audio/wav",
            headers={
                "Content-Type": "audio/wav",
                "Content-Length": str(len(audio_bytes))
            }
        )
    except Exception as e:
        print(f"❌ TTS Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# =========================================
# Optional: Re-load Knowledge Base on Demands
# =========================================
@app.route("/refreshkb", methods=["POST"])
def refresh_kb():
    """Reload Chroma collection without restarting the app."""
    global vector_store, retriever
    try:
        vector_store = Chroma(
            collection_name="ankit_rijal_kb",
            persist_directory="../chroma_db",
            embedding_function=embedding_function,
        )
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        print("🔄 Knowledge base refreshed successfully.")
        return jsonify({"response": "Knowledge base refreshed."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =========================================
# Cleanup on Exit
# =========================================
atexit.register(clear_chat_history)

# =========================================
# Run Server
# =========================================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
