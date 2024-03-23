"use client";

import { Icons } from "@/components/icons";
import IframeLoader from "@/components/interactive/IframeLoader"; // Adjust the import path as necessary
import { Message } from "ai/react";
import { useRef, useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { motion } from "framer-motion";
import { useChat } from "ai/react";

// @ts-ignore
const roleToColorMap: Record<Message["role"], string> = {
  system: "lightred",
  user: "white",
  function: "lightblue",
  assistant: "lightgreen",
};

const DotAnimation = () => {
  const dotVariants = {
    initial: { opacity: 0 },
    animate: { opacity: 1, transition: { duration: 0.5 } },
    exit: { opacity: 0, transition: { duration: 0.5 } },
  };

  // Stagger children animations
  const containerVariants = {
    initial: { transition: { staggerChildren: 0 } },
    animate: { transition: { staggerChildren: 0.5, staggerDirection: 1 } },
    exit: { transition: { staggerChildren: 0.5, staggerDirection: 1 } },
  };

  const [key, setKey] = useState(0);

  return (
    <motion.div
      key={key}
      initial="initial"
      animate="animate"
      exit="exit"
      className="flex gap-x-0.5 -ml-1"
      variants={containerVariants}
      onAnimationComplete={() => setKey((prevKey) => prevKey + 1)}
    >
      {[...Array(3)].map((_, i) => (
        <motion.span key={i} variants={dotVariants}>
          .
        </motion.span>
      ))}
    </motion.div>
  );
};

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit, error } = useChat();
  const [status, setStatus] = useState("idle"); // Add this line to create the status state
  const nohasReceivedResponse =
    messages.length === 0 || !messages.some((m) => m.role === "assistant");

  // const { messages, input, handleInputChange, handleSubmit, error } = useChat();
  // const [status, setStatus] = useState("idle");
  const [messageCount, setMessageCount] = useState(messages.length);

  // Call this function when you start waiting for a response
  const startWaitingForResponse = () => {
    setStatus("in_progress");
  };

  // Call this function when the response is received or an error occurs
  const stopWaitingForResponse = () => {
    setStatus("idle");
  };

  useEffect(() => {
    if (messages.length > messageCount + 1) {
      stopWaitingForResponse();
      setMessageCount(messages.length); // Update the message count
    }
  }, [messages.length, messageCount]);

  // Modify your handleSubmit function to use startWaitingForResponse
  const modifiedHandleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    startWaitingForResponse();
    handleSubmit(e); // Assuming handleSubmit will handle the async operation
    // Do not call stopWaitingForResponse here, useEffect will handle it
  };

  const messagesEndRef = useRef(null);

  // Effect for scrolling to the bottom of the chat
  useEffect(() => {
    setTimeout(() => {
      // @ts-ignore
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, 0); // Timeout set to 0 to delay scroll until after the render cycle
  }, [messages]);

  return (
    <main
      className={
        nohasReceivedResponse
          ? "flex min-h-screen flex-col p-24"
          : "flex min-h-screen p-24 justify-between"
      }
    >
      <div
        className={
          nohasReceivedResponse
            ? "flex flex-col w-full max-w-xl mx-auto stretch"
            : "flex flex-col w-2/5"
        }
      >
        <h1 className="text-3xl text-zinc-100 font-extrabold pb-4">
          Your AI Assistant 🤖
        </h1>
        {error && (
          <div className="relative bg-red-500 text-white px-6 py-4 rounded-md">
            <span className="block sm:inline">Error: {error.toString()}</span>
          </div>
        )}

        <div className="flex flex-col h-[700px] overflow-auto">
          {messages.map((m) => (
            <div
              key={m.id}
              className="whitespace-pre-wrap"
              style={{ color: roleToColorMap[m.role] }}
            >
              <strong>{`${m.role}: `}</strong>
              <ReactMarkdown>{m.content}</ReactMarkdown>
              <br />
            </div>
          ))}
          {/* Invisible element for scrolling into view */}
          {status === "in_progress" && (
            <span className="text-white flex gap-x-2">
              <Icons.spinner className="animate-spin w-5 h-5" />
              Processing
              <DotAnimation />
            </span>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form
          onSubmit={modifiedHandleSubmit}
          className="fixed bottom-0 w-full max-w-md p-2 mb-16 border border-gray-300 rounded shadow-xl bg-transparent"
        >
          <input
            className="w-full bg-transparent border-none placeholder-gray-400 text-white focus:ring-0"
            value={input}
            placeholder="Say something..."
            onChange={handleInputChange}
          />
        </form>
      </div>

      {!nohasReceivedResponse && <IframeLoader shouldDisplay={true} />}
    </main>
  );
}
