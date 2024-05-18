import React from 'react';
import ChatHeader from './ChatHeader';
import ChatMessages from './ChatMessages';
import ChatInput from './ChatInput';

const Chat = () => {
  return (
    <div className="z-0 w-[50%] flex flex-col rounded-lg bg-white justify-between">
      <div className="h-[80%] flex flex-col ">
        <ChatHeader></ChatHeader>
        <ChatMessages></ChatMessages>
      </div>

      <ChatInput className="h-[15%] p-3 z-0 flex items-end justify-center"></ChatInput>
    </div>
  );
};

export default Chat;
