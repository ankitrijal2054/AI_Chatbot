import React from 'react';

const VoiceInterface = ({ voiceState, onStartListening }) => {
  return (
    <div className="flex-grow flex items-center justify-center p-8">
      <div className="text-center">
        {voiceState === 'default' && (
          <div className="animate-scale-in">
            <button
              onClick={onStartListening}
              className="w-32 h-32 bg-gradient-to-br from-red-500 to-pink-500 hover:from-red-600 hover:to-pink-600 rounded-full shadow-2xl hover:shadow-red-500/50 transition-all duration-300 transform hover:scale-110 flex items-center justify-center group"
            >
              <svg className="w-16 h-16 text-white group-hover:scale-110 transition-transform" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
              </svg>
            </button>
            <p className="text-white/80 mt-6 text-lg font-medium">Click to speak</p>
          </div>
        )}

        {voiceState === 'listening' && (
          <div className="animate-scale-in">
            <div className="relative w-32 h-32 mx-auto">
              <div className="absolute inset-0 rounded-full bg-red-500/20 animate-ping"></div>
              <div className="absolute inset-0 rounded-full bg-red-500/40 animate-pulse"></div>
              <div className="relative w-full h-full rounded-full bg-gradient-to-br from-red-500 to-pink-500 flex items-center justify-center shadow-2xl">
                <div className="w-4 h-4 bg-white rounded-full animate-pulse"></div>
              </div>
            </div>
            <p className="text-white/80 mt-6 text-lg font-medium animate-pulse">Listening...</p>
          </div>
        )}

        {voiceState === 'processing' && (
          <div className="animate-scale-in">
            <div className="w-32 h-32 mx-auto rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center shadow-2xl">
              <div className="w-16 h-16 border-4 border-white/30 border-t-white rounded-full animate-spin"></div>
            </div>
            <p className="text-white/80 mt-6 text-lg font-medium">Processing...</p>
          </div>
        )}

        {voiceState === 'talking' && (
          <div className="animate-scale-in">
            <div className="w-32 h-32 mx-auto rounded-full bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center shadow-2xl">
              <div className="flex items-end justify-center gap-1 h-12">
                {[...Array(5)].map((_, i) => (
                  <div
                    key={i}
                    className="w-2 bg-white rounded-full animate-pulse"
                    style={{
                      height: '100%',
                      animationDelay: `${i * 0.1}s`,
                      animationDuration: '0.6s',
                    }}
                  ></div>
                ))}
              </div>
            </div>
            <p className="text-white/80 mt-6 text-lg font-medium animate-pulse">Speaking...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default VoiceInterface;
