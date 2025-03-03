import React, { useState, useEffect, useRef } from "react";
import "./App.css";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isThinking, setIsThinking] = useState(false);
  const [displayedMessage, setDisplayedMessage] = useState("");
  const chatContainerRef = useRef(null);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [messages, displayedMessage]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");
    setIsThinking(true);
    setDisplayedMessage("");

    try {
      const response = await fetch("http://localhost:5001/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: input }),
      });
      const data = await response.json();
      setIsThinking(false);
      displayTypewriterEffect(data.response);
    } catch (error) {
      console.error("Error fetching response:", error);
      setIsThinking(false);
    }
  };

  const clear_chat_history = async () => {
    try {
      const response = await fetch("http://localhost:5001/clearchat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();
      console.log(data.response);
    } catch (error) {
      console.error("Error clearing chat:", error);
    }
  };

  const displayTypewriterEffect = (text) => {
    let index = -1;
    setDisplayedMessage("");
    const interval = setInterval(() => {
      if (index + 1 < text.length) {
        index++;
        setDisplayedMessage((prev) => prev + text.charAt(index));
      } else {
        clearInterval(interval);
        setMessages((prevMessages) => [
          ...prevMessages,
          { role: "assistant", content: text },
        ]);
        setDisplayedMessage("");
      }
    }, 15);
  };

  const clearChat = () => {
    clear_chat_history();
    setMessages([]);
    setDisplayedMessage("");
  };

  return (
    <div className="chat-container">
      <h1 className="title">Ankit's AI Chat Assistant</h1>
      <div className="chat-box">
        <div className="chat-content" ref={chatContainerRef}>
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`message ${
                msg.role === "user" ? "user-msg" : "assistant-msg"
              }`}
            >
              <p>{msg.content}</p>
            </div>
          ))}
          {isThinking && (
            <div className="message assistant-msg">
              <p>
                Thinking<span className="dots">...</span>
              </p>
            </div>
          )}
          {displayedMessage && (
            <div className="message assistant-msg">
              <p>{displayedMessage}</p>
            </div>
          )}
        </div>
      </div>
      <div className="input-box">
        {messages.length > 0 && (
          <button className="clear-btn" onClick={clearChat}>
            🗑️
          </button>
        )}
        <input
          type="text"
          className="chat-input"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && sendMessage()}
        />
        <button className="send-btn" onClick={sendMessage}>
          ➤
        </button>
      </div>
    </div>
  );
};

export default App;
