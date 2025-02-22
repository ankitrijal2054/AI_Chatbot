from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Load API keys from Railway environment variables
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")

embedding_function = HuggingFaceInferenceAPIEmbeddings(
    api_key=HUGGINGFACE_API_KEY,
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Initialize ChromaDB with persistent storage
vector_store = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
retriever = vector_store.as_retriever()

# Function to get response from Grok AI
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

    # Retrieve relevant context from ChromaDB
    retrieved_docs = retriever.get_relevant_documents(user_query)
    retrieved_text = "\n".join([doc.page_content for doc in retrieved_docs])
    
    print(f"Retrieved text: {retrieved_text}")

    # Combine retrieved knowledge with the query
    full_query = f'''Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
\n{retrieved_text}\n\n Note 1: If the context provided does not contain information relevant to the question, then reply as a normal chatbot.\n
Note 2: If the context provided contains information relevant to the question, then reply as a first person based on the context.\n
Note 3: When answering the question, make sure to provide a clear and concise response. And do not say that you are replying based on context.\n
Note 4: Properly format your response to the question.\n
\n\nQuestion: {user_query}'''

    # Get response from Grok AI
    response = chat_with_ai(full_query)
    
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))
