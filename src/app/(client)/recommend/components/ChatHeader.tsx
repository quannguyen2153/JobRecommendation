import { FC } from 'react';

const ChatHeader: FC = () => {
  return (
    <div className="w-full flex rounded-lg gap-3 justify-start items-center text-zinc-800 mb-4">
      <div className="w-full rounded-t-lg flex flex-col items-start text-sm p-6 bg-gradient-to-r from-primary to-primary-200">
        <div className="flex gap-1.5 items-center">
          <p className="w-4 h-4 rounded-full bg-green-500" />
          <p className="font-normal text-lg text-white">CV Improver Bot</p>
        </div>
        <p className="font-normal text-md text-white">
          We're here to help you!
        </p>
      </div>
    </div>
  );
};

export default ChatHeader;
