import React from 'react';

const WelcomeScreen = ({ onStartChat }) => {
  return (
    <div className="flex items-center justify-center min-h-screen p-4 animate-fade-in">
      <div className="max-w-2xl w-full">
        {/* Frosted Glass Card */}
        <div className="bg-white/10 dark:bg-black/20 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-8 md:p-12 animate-scale-in">
          {/* Logo/Icon */}
          <div className="flex justify-center mb-8">
            <div className="w-24 h-24 bg-gradient-to-br from-purple-500 to-pink-500 rounded-3xl flex items-center justify-center shadow-lg animate-float">
              <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
          </div>

          {/* Welcome Text */}
          <h1 className="text-4xl md:text-5xl font-bold text-center mb-4 bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
            Welsome To My Personal AI Chatbot
          </h1>
          
          <p className="text-center text-white/80 text-lg md:text-xl mb-8 leading-relaxed">
            Curious about my journey, projects, or skills? This chatbot is designed to share 
  insights about me. From my background and professional experience to the things 
  I’m passionate about. Start a conversation and get to know me better!
          </p>

          {/* Features */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10 hover:bg-white/10 transition-all duration-300">
              <div className="text-3xl mb-2">🚀</div>
              <h3 className="text-white font-semibold mb-1">Fast & Smart</h3>
              <p className="text-white/60 text-sm">Instant AI-powered responses using RAG</p>
            </div>
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10 hover:bg-white/10 transition-all duration-300">
              <div className="text-3xl mb-2">🎯</div>
              <h3 className="text-white font-semibold mb-1">Contextual</h3>
              <p className="text-white/60 text-sm">Remembers conversation history</p>
            </div>
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10 hover:bg-white/10 transition-all duration-300">
              <div className="text-3xl mb-2">🎤</div>
              <h3 className="text-white font-semibold mb-1">Voice Mode</h3>
              <p className="text-white/60 text-sm">Speak and listen naturally</p>
            </div>
          </div>

          {/* Start Button */}
          <button
            onClick={onStartChat}
            className="w-full bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 hover:from-purple-600 hover:via-pink-600 hover:to-blue-600 text-white font-bold py-4 px-8 rounded-2xl shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all duration-300 text-lg"
          >
            Start Chatting
            <span className="ml-2">→</span>
          </button>

          {/* Footer Note */}
          <p className="text-center text-white/40 text-sm mt-6">
            Powered by Google Gemini AI
          </p>
        </div>
      </div>
    </div>
  );
};

export default WelcomeScreen;
