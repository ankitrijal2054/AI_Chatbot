# AI Chatbot

This is a custom AI chatbot application built using **React.js** for the frontend and **Flask** for the backend. The chatbot leverages **LangChain** for retrieval-augmented generation (RAG) using **ChromaDB** as a vector store, and it integrates with **Hugging Face** and **Grok AI** for embeddings and responses.

## Features

- Uses **ChromaDB** to retrieve relevant context from a knowledge base.
- Implements **Hugging Face embeddings** for vector search.
- Connects to **Grok AI** to generate responses.
- Supports **real-time chatting** with a smooth UI experience.
- Includes **typewriter effect** for chatbot responses.
- **CORS-enabled Flask backend** to communicate with the frontend.

---

## Screenshots

![Chat Interface1](screenshots/chat1.png)

![Chat Interface2](screenshots/chat2.png)

---

## Tech Stack

### Frontend

- **React.js** (with Hooks & State Management)
- **CSS** (for styling)
- **Fetch API** (to communicate with backend)

### Backend

- **Flask** (REST API framework)
- **Flask-CORS** (for handling cross-origin requests)
- **LangChain** (for vector search and embeddings)
- **ChromaDB** (for vector storage)
- **Hugging Face** (for embeddings API)
- **Grok AI API** (for chatbot responses)

---

## Installation & Setup

### Prerequisites

- Node.js and npm (for frontend)
- Python 3.8+ (for backend)
- Virtual environment (`venv`) for Python (recommended)
- API keys for **Hugging Face** and **Grok AI** stored in `api_key.json` in the backend.

### Backend Setup

1. Clone this repository:

   ```sh
   git clone https://github.com/ankitrijal2054/AI_Chatbot.git
   cd AI-Chatbot
   ```

2. Navigate to the backend directory:

   ```sh
   cd backend
   ```

3. Create and activate a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows, use: venv\Scripts\activate
   ```

4. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

5. Add your API keys in a file called `api_key.json`:

   ```json
   {
     "HUGGINGFACE_API_KEY": "your-huggingface-api-key",
     "XAI_API_KEY": "your-grok-ai-api-key"
   }
   ```

6. Run the backend server:
   ```sh
   python chatbot.py
   ```
   The Flask server should now be running on `http://localhost:5001`.

---

### Frontend Setup

1. Navigate to the frontend directory:

   ```sh
   cd frontend
   ```

2. Install dependencies:

   ```sh
   npm install
   ```

3. Start the frontend application:
   ```sh
   npm start
   ```
   The React app should now be running on `http://localhost:3000`.

---

## Usage

1. Open the React frontend (`http://localhost:3000`).
2. Type a message in the input box and press **Enter** or click the send button.
3. The chatbot will respond using retrieved knowledge and AI-generated text.
4. Click the 🗑️ button to clear the chat history.

---

## Future Improvements

- Deploy frontend & backend to **Railway**.
- Add support for **memory-based conversations**.
- Improve **error handling & logging**.

---

## Contributing

Pull requests are welcome! If you find any issues, please open an **issue** or submit a **PR**.

---

## License

This project is licensed under the **MIT License**.

---

## Author

**Ankit Rijal**
