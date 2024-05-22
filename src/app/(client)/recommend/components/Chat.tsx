import React, { useEffect, useState } from 'react';
import ChatHeader from './ChatHeader';
import ChatMessages from './ChatMessages';
import ChatInput from './ChatInput';
import { nanoid } from 'nanoid';

const defaultValue = [
  {
    id: nanoid(),
    message: 'Hello, how can I help you?',
    jobId: 1,
    isUserMessage: false,
  },
];

const Chat = ({ selectedJob }) => {
  const [messages, setMessages] = useState<Message[]>(defaultValue);
  console.log('🚀 ~ Chat ~ messages:', messages);
  const [isMessageUpdating, setIsMessageUpdating] = useState<boolean>(false);

  useEffect(() => {
    setMessages(defaultValue);
  }, [selectedJob]);

  return (
    <div className="w-full h-[70%] z-0  flex flex-col rounded-lg bg-white justify-between shadow-lg drop-shadow-lg">
      <div className="h-[80%] flex flex-col z-0">
        <ChatHeader></ChatHeader>
        <ChatMessages messages={messages}></ChatMessages>
      </div>

      {isMessageUpdating && (
        <div className="text-slate-500 font-semibold text-md ml-3 flex flex-row gap-2 items-center">
          <p>Chatbot is answering</p>
          <div className="h-3 w-3 bg-slate-500 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
          <div className="h-3 w-3 bg-slate-500 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
          <div className="h-3 w-3 bg-slate-500 rounded-full animate-bounce"></div>
        </div>
      )}

      <ChatInput
        className="h-[15%] p-3 z-0 flex items-end justify-center"
        selectedJob={selectedJob}
        messages={messages}
        setMessages={setMessages}
        isMessageUpdating={isMessageUpdating}
        setIsMessageUpdating={setIsMessageUpdating}
      ></ChatInput>
    </div>
  );
};

export default Chat;
