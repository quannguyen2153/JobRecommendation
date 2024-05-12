'use client';
import React from 'react';
import { useEffect, useRef, useState } from 'react';
import toast from 'react-hot-toast';
import { ScrollArea } from '@radix-ui/react-scroll-area';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button, Input } from '@nextui-org/react';
import { SendHorizontalIcon } from 'lucide-react';
import { useChat } from 'ai/react';

const ChatbotPopup = () => {
  const ref = useRef<HTMLDivElement>(null);
  const { messages, input, handleInputChange, handleSubmit, isLoading, error } =
    useChat({
      initialMessages: [
        {
          id: Date.now().toString(),
          role: 'system',
          content: 'You are an assistant that gives short answers.',
        },
      ],

      onResponse: (response) => {
        if (!response.ok) {
          const status = response.status;

          switch (status) {
            case 401:
              // openSignIn()
              break;
            default:
              toast.error(error?.message || 'Something went wrong!');
              break;
          }
        }
        //   session?.reload()
      },
    });

  useEffect(() => {
    if (ref.current === null) return;
    ref.current.scrollTo(0, ref.current.scrollHeight);
  }, [messages]);

  function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    //   if (isSignedIn) {
    //     handleSubmit(e)
    //   } else {
    //     openSignIn()
    //   }
    handleSubmit(e);
  }

  return (
    <div className="container max-w-3xl">
      {/* Chat area */}
      <div
        className="mx-auto mt-3 w-full max-w-lg  hover:shadow-inner  p-4 
 rounded-md outline outline-primary outline-offset-2 drop-shadow-md"
      >
        <ScrollArea className="mb-2 h-[400px] rounded-md " ref={ref}>
          {messages.map((m) => (
            <div key={m.id} className="mr-6 whitespace-pre-wrap md:mr-12">
              {m.role === 'user' && (
                <div className="mb-6 flex gap-3">
                  <Avatar>
                    <AvatarImage src="" />
                    <AvatarFallback className="text-sm">U</AvatarFallback>
                  </Avatar>
                  <div className="mt-1.5">
                    <p className="font-semibold">You</p>
                    <div className="mt-1.5 text-sm text-zinc-500">
                      {m.content}
                    </div>
                  </div>
                </div>
              )}

              {m.role === 'assistant' && (
                <div className="mb-6 flex gap-3">
                  <Avatar>
                    <AvatarImage src="" />
                    <AvatarFallback className="bg-emerald-500 text-white">
                      AI
                    </AvatarFallback>
                  </Avatar>
                  <div className="mt-1.5 w-full">
                    <div className="mt-2 text-sm text-zinc-500">
                      {m.content}
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </ScrollArea>

        <form
          onSubmit={onSubmit}
          className="relative flex flex-row justify-between"
        >
          <Input
            name="message"
            value={input}
            onChange={handleInputChange}
            placeholder={'Ask me anything...'}
            className="w-[75%] placeholder:italic placeholder:text-zinc-600/75 focus-visible:ring-zinc-500"
          />
          <Button
            size="md"
            type="submit"
            variant="solid"
            disabled={isLoading}
            className="w-[20%]  bg-primary"
          >
            <SendHorizontalIcon className="h-5 w-5 text-white" />
          </Button>
        </form>
      </div>
    </div>
  );
};

export default ChatbotPopup;
