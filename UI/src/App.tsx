import React, { useEffect, useState, useRef } from "react";
import { Send, Compass, Target, Sparkles } from "lucide-react";
import { ChatMessage } from "./components/ChatMessage";
export function App() {
  const [messages, setMessages] = useState([
    {
      isAi: true,
      message:
        "Hi there! I'm your AI Career Guide. I'm here to help you explore career paths based on your interests and aspirations. To get started, could you tell me about what kind of work interests you the most? For example, do you enjoy being creative, solving technical problems, working with people, or something else?",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  };
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    setMessages((prev) => [
      ...prev,
      {
        isAi: false,
        message: input,
      },
    ]);
    setInput("");
    setIsLoading(true);
    try {
      const response = await fetch("https://fd60-2601-646-a180-6c90-9c08-cf74-bc06-f6f8.ngrok-free.app/ai", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: input.trim(),
        }),
      });
      if (!response.ok) {
        throw new Error("API request failed");
      }
      const data = await response.json();

      console.log(data);
      
      setMessages((prev) => [
        ...prev,
        {
          isAi: true,
          message: data.answer,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          isAi: true,
          message: "I apologize, but I'm having trouble connecting right now. Please try again later.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <div className="flex flex-col w-full h-screen bg-gradient-to-b from-slate-800 via-blue-900 to-slate-900">
      <header className="w-full bg-slate-800/50 backdrop-blur-sm shadow-lg border-b border-slate-700/50 flex-none">
        <div className="max-w-3xl mx-auto p-8 text-center">
          <div className="flex items-center justify-center gap-3 mb-3">
            <div className="relative">
              <div className="absolute -inset-1 rounded-full bg-gradient-to-r from-blue-500 to-indigo-600 opacity-75 blur"></div>
              <div className="relative bg-slate-900 rounded-full p-2">
                <Compass className="w-10 h-10 text-blue-400" />
              </div>
            </div>
            <h1 className="text-3xl font-semibold bg-gradient-to-r from-blue-400 to-indigo-400 text-transparent bg-clip-text">
              Career Compass AI
            </h1>
          </div>
          <p className="text-slate-400">
            Your personal guide to professional discovery
          </p>
        </div>
      </header>
      <main className="flex-1 w-full max-w-3xl mx-auto p-4 relative min-h-0">
        <div className="absolute top-20 right-8 opacity-10">
          <Target className="w-24 h-24 text-blue-400" />
        </div>
        <div className="absolute bottom-20 left-8 opacity-10">
          <Sparkles className="w-20 h-20 text-indigo-400" />
        </div>
        <div className="relative z-10 bg-slate-800/50 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-700/50 p-6 h-full flex flex-col">
          <div className="flex-1 min-h-0">
            <div className="h-full overflow-y-auto pr-2">
              <div className="space-y-4">
                {messages.map((msg, index) => (
                  <ChatMessage
                    key={index}
                    isAi={msg.isAi}
                    message={msg.message}
                  />
                ))}
                {isLoading && (
                  <ChatMessage
                    isAi={true}
                    message="Thinking..."
                    // isLoading={true}
                  />
                )}
                <div ref={messagesEndRef} />
              </div>
            </div>
          </div>
          <form
            onSubmit={handleSubmit}
            className="flex gap-2 pt-4 border-t border-slate-700/50 flex-none"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              disabled={isLoading}
              className="flex-1 p-4 rounded-xl border border-slate-700 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all bg-slate-800/50 text-slate-200 placeholder-slate-400 disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={isLoading}
              className="p-4 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-xl hover:opacity-90 transition-all hover:shadow-lg hover:shadow-blue-500/20 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send size={20} />
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}
