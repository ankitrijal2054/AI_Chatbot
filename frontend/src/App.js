import React, { useState, useEffect, useRef, useCallback } from "react";
import AnimatedBackground from "./components/AnimatedBackground";
import WelcomeScreen from "./components/WelcomeScreen";
import ChatInterface from "./components/ChatInterface";
import VoiceInterface from "./components/VoiceInterface";

const App = () => {
  const [showWelcome, setShowWelcome] = useState(true);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isThinking, setIsThinking] = useState(false);
  const [displayedMessage, setDisplayedMessage] = useState("");
  const [isVoiceMode, setIsVoiceMode] = useState(false);
  const [voiceState, setVoiceState] = useState("default");
  const [isDarkMode, setIsDarkMode] = useState(true);
  const chatContainerRef = useRef(null);

  // Apply dark mode class to document
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
      document.body.classList.remove('light-mode');
    } else {
      document.documentElement.classList.remove('dark');
      document.body.classList.add('light-mode');
    }
  }, [isDarkMode]);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages.length, displayedMessage]);

  const displayTypewriterEffect = useCallback((text) => {
    let index = -1;
    setDisplayedMessage("");
    const typeNext = () => {
      if (index + 1 < text.length) {
        setDisplayedMessage((prev) => prev + text.charAt(index));
        index++;
        setTimeout(typeNext, 15);
      } else {
        setMessages((prevMessages) => [
          ...prevMessages,
          { role: "assistant", content: text },
        ]);
        setDisplayedMessage("");
      }
    };
    typeNext();
  }, []);

  const sendMessage = useCallback(async () => {
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
  }, [input, messages, displayTypewriterEffect]);

  const clearChatHistoryAPI = useCallback(async () => {
    try {
      const response = await fetch("http://localhost:5001/clearchat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error("Error clearing chat:", error);
    }
  }, []);

  const clearChat = useCallback(() => {
    clearChatHistoryAPI();
    setMessages([]);
    setDisplayedMessage("");
  }, [clearChatHistoryAPI]);

  const speakResponse = useCallback(async (text) => {
    try {
      const response = await fetch("http://localhost:5001/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }
      
      const audioBlob = await response.blob();
      
      // Check if blob has valid content
      if (audioBlob.size === 0) {
        throw new Error("Received empty audio response");
      }
      
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      
      audio.onerror = (e) => {
        console.error("Audio playback error:", e);
        setVoiceState("default");
        URL.revokeObjectURL(audioUrl);
      };
      
      audio.onended = () => {
        setVoiceState("default");
        URL.revokeObjectURL(audioUrl);
      };
      
      setVoiceState("talking");
      await audio.play();
    } catch (error) {
      console.error("Error synthesizing voice response:", error);
      setVoiceState("default");
      alert(`Voice synthesis error: ${error.message}`);
    }
  }, []);

  const startVoiceRecognition = useCallback(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Sorry, your browser does not support speech recognition.");
      return;
    }
    
    // Request microphone permission first
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(() => {
        const recognition = new SpeechRecognition();
        recognition.lang = "en-US";
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onstart = () => {
          setVoiceState("listening");
        };

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
            alert("Failed to get response. Please try again.");
          }
        };

        recognition.onerror = (event) => {
          console.error("Speech recognition error:", event.error);
          let errorMessage = "Speech recognition error: ";
          
          switch(event.error) {
            case 'audio-capture':
              errorMessage += "No microphone was found or microphone access was denied.";
              break;
            case 'not-allowed':
              errorMessage += "Microphone permission was denied. Please allow microphone access.";
              break;
            case 'no-speech':
              errorMessage += "No speech was detected. Please try again.";
              break;
            case 'network':
              errorMessage += "Network error occurred.";
              break;
            default:
              errorMessage += event.error;
          }
          
          alert(errorMessage);
          setVoiceState("default");
        };
        
        recognition.onend = () => {
          if (voiceState === "listening") {
            setVoiceState("default");
          }
        };
        
        try {
          recognition.start();
        } catch (error) {
          console.error("Error starting recognition:", error);
          setVoiceState("default");
          alert("Failed to start speech recognition. Please try again.");
        }
      })
      .catch((error) => {
        console.error("Microphone permission error:", error);
        alert("Microphone access denied. Please allow microphone access in your browser settings.");
        setVoiceState("default");
      });
  }, [speakResponse, voiceState]);

  const handleStartChat = () => {
    setShowWelcome(false);
  };

  if (showWelcome) {
    return (
      <>
        <AnimatedBackground />
        <WelcomeScreen onStartChat={handleStartChat} />
      </>
    );
  }

  return (
    <>
      <AnimatedBackground />
      
      <div className="min-h-screen flex items-center justify-center p-4 animate-fade-in">
        <div className="w-full max-w-5xl h-[85vh] flex flex-col">
          {/* Header */}
          <div className="bg-white/10 dark:bg-black/20 backdrop-blur-xl border border-white/20 dark:border-white/20 border-gray-800/30 rounded-t-3xl p-4 shadow-lg animate-slide-down">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center shadow-lg">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                  </svg>
                </div>
                <div>
                  <h1 className="text-lg font-bold text-gray-900 dark:text-white">AI Chat Assistant</h1>
                  <p className="text-xs text-gray-600 dark:text-white/60">Powered by Gemini AI</p>
                </div>
              </div>
              
              <div className="flex items-center gap-2">
                {/* Dark/Light Mode Toggle */}
                <button
                  onClick={() => setIsDarkMode(!isDarkMode)}
                  className="w-10 h-10 rounded-xl bg-white/5 hover:bg-white/10 dark:bg-white/5 dark:hover:bg-white/10 bg-gray-800/20 hover:bg-gray-800/30 border border-white/20 dark:border-white/20 border-gray-800/30 flex items-center justify-center transition-all duration-300"
                  title={isDarkMode ? "Light mode" : "Dark mode"}
                >
                  {isDarkMode ? (
                    <svg className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clipRule="evenodd" />
                    </svg>
                  ) : (
                    <svg className="w-5 h-5 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                    </svg>
                  )}
                </button>

                {/* Voice/Text Mode Toggle */}
                <button
                  onClick={() => setIsVoiceMode(!isVoiceMode)}
                  className="px-4 py-2 rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white text-sm font-medium transition-all duration-300 shadow-lg hover:shadow-purple-500/50 flex items-center gap-2"
                >
                  {isVoiceMode ? (
                    <>
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
                      </svg>
                      <span className="hidden sm:inline">Text Mode</span>
                    </>
                  ) : (
                    <>
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
                      </svg>
                      <span className="hidden sm:inline">Voice Mode</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Main Chat Container */}
          <div className="flex-grow bg-white/5 dark:bg-black/10 bg-white/50 backdrop-blur-xl border-x border-white/20 dark:border-white/20 border-gray-800/30 overflow-hidden animate-slide-up">
            {isVoiceMode ? (
              <VoiceInterface 
                voiceState={voiceState} 
                onStartListening={startVoiceRecognition}
              />
            ) : (
              <ChatInterface
                messages={messages}
                displayedMessage={displayedMessage}
                isThinking={isThinking}
                input={input}
                setInput={setInput}
                onSendMessage={sendMessage}
                onClearChat={clearChat}
                chatContainerRef={chatContainerRef}
              />
            )}
          </div>

          {/* Footer */}
          <div className="bg-white/10 dark:bg-black/20 backdrop-blur-xl border border-white/20 dark:border-white/20 border-gray-800/30 rounded-b-3xl p-3 shadow-lg animate-slide-up">
            <div className="flex items-center justify-center gap-2 text-xs text-gray-600 dark:text-white/40">
              <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z" clipRule="evenodd" />
              </svg>
              <span>Powered by Gemini AI</span>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default App;
