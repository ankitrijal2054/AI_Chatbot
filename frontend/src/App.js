import React, { useState, useEffect, useRef } from "react";
import "./App.css";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isThinking, setIsThinking] = useState(false);
  const [displayedMessage, setDisplayedMessage] = useState("");
  const [isVoiceMode, setIsVoiceMode] = useState(false);
  // Voice UI states: "default", "listening", "processing", "talking"
  const [voiceState, setVoiceState] = useState("default");
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
        headers: { "Content-Type": "application/json" },
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

  // Function to start voice recognition with updated UI states
  const startVoiceRecognition = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Sorry, your browser does not support speech recognition.");
      return;
    }
    setVoiceState("listening");
    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = async (event) => {
      const transcript = event.results[0][0].transcript;
      setVoiceState("processing");
      try {
        const response = await fetch("http://localhost:5001/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: transcript }),
        });
        const data = await response.json();
        await speakResponse(data.response);
      } catch (error) {
        console.error("Error fetching voice response:", error);
        setVoiceState("default");
      }
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
      setVoiceState("default");
    };
  };

  // Function to fetch synthesized audio from the /tts endpoint and play it
  const speakResponse = async (text) => {
    try {
      const response = await fetch("http://localhost:5001/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.onended = () => {
        setVoiceState("default");
      };
      setVoiceState("talking");
      audio.play();
    } catch (error) {
      console.error("Error synthesizing voice response:", error);
      setVoiceState("default");
    }
  };

  return (
    <div className="chat-container">
      <h1 className="title">Ankit's AI Chat Assistant</h1>
      <div className="toggle-container">
        <button
          className="toggle-btn"
          onClick={() => setIsVoiceMode(!isVoiceMode)}
        >
          {isVoiceMode ? "Switch to Text Chat" : "Switch to Voice Chat"}
        </button>
      </div>
      {isVoiceMode ? (
        <div className="voice-chat-container">
          {voiceState === "default" && (
            <button className="voice-btn" onClick={startVoiceRecognition}>
              Click to Speak
            </button>
          )}
          {voiceState === "listening" && (
            <div className="fancy-listening">
              <div className="listening-circle"></div>
            </div>
          )}
          {voiceState === "processing" && (
            <div className="fancy-processing">
              <div className="spinner"></div>
            </div>
          )}
          {voiceState === "talking" && (
            <div className="fancy-talking">
              <div className="talking-wave">
                <div className="bar"></div>
                <div className="bar"></div>
                <div className="bar"></div>
                <div className="bar"></div>
                <div className="bar"></div>
              </div>
            </div>
          )}
        </div>
      ) : (
        <>
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
        </>
      )}
    </div>
  );
};

export default App;
