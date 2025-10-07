import React from 'react';
import Message from './Message';

const ChatInterface = ({ 
  messages, 
  displayedMessage, 
  isThinking, 
  input, 
  setInput, 
  onSendMessage, 
  onClearChat,
  chatContainerRef 
}) => {
  return (
    <div className="flex flex-col h-full">
      {/* Chat Messages Container */}
      <div 
        ref={chatContainerRef}
        className="flex-grow overflow-y-auto px-4 py-6 space-y-4 scroll-smooth scrollbar-thin scrollbar-thumb-white/20 scrollbar-track-transparent hover:scrollbar-thumb-white/30"
      >
        {messages.length === 0 && !isThinking && !displayedMessage && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center animate-fade-in">
              <div className="text-6xl mb-4 animate-float">💬</div>
              <h3 className="text-white/60 text-lg font-medium">Start a conversation</h3>
              <p className="text-white/40 text-sm mt-2">Ask me anything!</p>
            </div>
          </div>
        )}

        {messages.map((msg, index) => (
          <Message key={index} msg={msg} />
        ))}

        {isThinking && (
          <div className="flex justify-start mb-4 animate-fade-in">
            <div className="flex items-end gap-2 max-w-[80%]">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 flex items-center justify-center">
                <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <div className="px-4 py-3 rounded-2xl rounded-bl-sm bg-white/10 backdrop-blur-md border border-white/20">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></div>
                  <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}

        {displayedMessage && (
          <Message msg={{ role: 'assistant', content: displayedMessage }} isTyping={true} />
        )}
      </div>

      {/* Input Box */}
      <div className="p-4 border-t border-white/10 bg-black/20 backdrop-blur-sm">
        <div className="flex items-center gap-2 bg-white/5 backdrop-blur-md border border-white/20 rounded-2xl p-2 focus-within:border-purple-500/50 transition-all duration-300">
          {messages.length > 0 && (
            <button
              onClick={onClearChat}
              className="flex-shrink-0 w-10 h-10 rounded-xl bg-red-500/20 hover:bg-red-500/30 text-red-400 hover:text-red-300 transition-all duration-300 flex items-center justify-center group"
              title="Clear chat"
            >
              <svg className="w-5 h-5 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          )}
          
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && onSendMessage()}
            placeholder="Type your message..."
            className="flex-grow bg-transparent text-white placeholder-white/40 outline-none px-3 py-2 text-sm md:text-base"
          />
          
          <button
            onClick={onSendMessage}
            disabled={!input.trim()}
            className="flex-shrink-0 w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 disabled:from-gray-500 disabled:to-gray-600 disabled:opacity-50 disabled:cursor-not-allowed text-white transition-all duration-300 flex items-center justify-center shadow-lg hover:shadow-purple-500/50 transform hover:scale-105 disabled:hover:scale-100"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
