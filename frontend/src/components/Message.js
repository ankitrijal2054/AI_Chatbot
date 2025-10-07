import React from 'react';

const Message = React.memo(({ msg, isTyping }) => {
  const isUser = msg.role === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 animate-fade-in`}>
      <div className={`flex items-end gap-2 max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser 
            ? 'bg-gradient-to-br from-purple-500 to-pink-500' 
            : 'bg-white/10 backdrop-blur-sm border border-white/20'
        }`}>
          {isUser ? (
            <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
            </svg>
          ) : (
            <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          )}
        </div>

        {/* Message Bubble */}
        <div className={`px-4 py-3 rounded-2xl shadow-lg transition-all duration-300 ${
          isUser
            ? 'bg-gradient-to-br from-purple-500 to-pink-500 text-white rounded-br-sm'
            : 'bg-white/10 backdrop-blur-md border border-white/20 text-white rounded-bl-sm hover:bg-white/15'
        }`}>
          <p className="text-sm md:text-base leading-relaxed whitespace-pre-wrap break-words">
            {msg.content}
            {isTyping && <span className="inline-block w-1 h-4 ml-1 bg-current animate-pulse"></span>}
          </p>
        </div>
      </div>
    </div>
  );
});

export default Message;
