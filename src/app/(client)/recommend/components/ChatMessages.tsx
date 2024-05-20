'use client';

import { cn } from '@/lib/utils';
import { ScrollShadow } from '@nextui-org/react';
import {
  FC,
  HTMLAttributes,
  useContext,
  useEffect,
  useRef,
  useState,
} from 'react';

interface ChatMessagesProps extends HTMLAttributes<HTMLDivElement> {
  messages: Message[];
}

const ChatMessages: FC<ChatMessagesProps> = ({
  className,
  messages,
  ...props
}) => {
  const inverseMessages = [...messages].reverse();

  // Scroll to bottom when new message is added
  const chatContainerRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  //Multiple drop lines
  function MultipleLinesParagraph(text: string) {
    const descriptionWithLineBreaks = text.split('\n').map((text, index) => (
      <span key={index}>
        {text}
        <br />
      </span>
    ));

    return <p>{descriptionWithLineBreaks}</p>;
  }

  // Typing effect
  const [displayResponse, setDisplayResponse] = useState('');
  const [completedTyping, setCompletedTyping] = useState(false);

  useEffect(() => {
    setCompletedTyping(false);

    let i = 0;
    const stringResponse = inverseMessages[inverseMessages.length - 1].message;

    const intervalId = setInterval(() => {
      setDisplayResponse(stringResponse.slice(0, i));

      i++;

      if (i > stringResponse.length) {
        clearInterval(intervalId);
        setCompletedTyping(true);
      }
    }, 20);

    return () => clearInterval(intervalId);
  }, [inverseMessages]);
  return (
    <ScrollShadow
      ref={chatContainerRef}
      isEnabled={false}
      hideScrollBar
      className={cn('h-[600px] p-2', className)}
    >
      <div {...props} className={cn('flex flex-col-reverse gap-3 ', className)}>
        <div className="flex-1" />
        {inverseMessages.map((message) => {
          return (
            <div
              className="chat-message"
              key={`${message.jobId}-${message.message}`}
            >
              <div
                className={cn('flex items-end', {
                  'justify-end': message.isUserMessage,
                })}
              >
                <div
                  className={cn(
                    'flex flex-col space-y-2 text-sm max-w-xl mx-2 overflow-x-hidden shadow-md rounded-lg',
                    {
                      'order-1 items-end': message.isUserMessage,
                      'order-2 items-start': !message.isUserMessage,
                    }
                  )}
                >
                  <p
                    className={cn('px-4 py-2 rounded-lg', {
                      'bg-gradient-to-r from-primary-400 to-primary text-white':
                        message.isUserMessage,
                      'bg-gradient-to-l from-slate-400 to-slate-500 text-zinc-100':
                        !message.isUserMessage,
                    })}
                  >
                    {MultipleLinesParagraph(message.message)}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>{' '}
    </ScrollShadow>
  );
};

export default ChatMessages;
