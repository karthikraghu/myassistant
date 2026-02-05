"use client";

import { useState } from "react";
import ChatInput from "@/components/ChatInput";
import ChatMessage from "@/components/ChatMessage";
import { Card } from "@/components/ui/card";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: content }),
      });

      const data = await response.json();

      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: data.response || "No response received.",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: "Failed to connect to the assistant. Is the backend running?",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex flex-col p-6 max-w-3xl mx-auto">
      {/* Header */}
      <Card className="text-center p-6 mb-6 border-[3px] border-foreground shadow-[4px_4px_0_var(--foreground)]">
        <h1 className="text-2xl font-bold tracking-tight">Personal Assistant</h1>
        <p className="text-muted-foreground text-sm mt-1">Your AI-powered helper</p>
        <div className="inline-flex items-center gap-2 mt-3 px-3 py-1 bg-primary border-2 border-foreground text-primary-foreground text-xs font-semibold uppercase">
          <span className="w-2 h-2 bg-foreground rounded-full animate-pulse" />
          Online
        </div>
      </Card>

      {/* Chat Container */}
      <Card className="flex-1 flex flex-col border-[3px] border-foreground shadow-[4px_4px_0_var(--foreground)] overflow-hidden">
        {/* Messages */}
        <div className="flex-1 p-6 overflow-y-auto flex flex-col gap-4 min-h-[400px] max-h-[60vh] bg-background">
          {messages.length === 0 && (
            <div className="text-center text-muted-foreground m-auto p-6">
              <p className="mb-4 font-medium">How can I help you today?</p>
              <ul className="space-y-2 max-w-xs mx-auto">
                {["Check my schedule", "Read my emails", "Plan my day"].map((item) => (
                  <li
                    key={item}
                    className="p-3 bg-card border-2 border-foreground text-foreground text-sm cursor-pointer transition-all hover:bg-primary hover:shadow-[2px_2px_0_var(--foreground)] hover:translate-x-[-2px] hover:translate-y-[-2px]"
                  >
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          )}
          {messages.map((msg) => (
            <ChatMessage key={msg.id} message={msg} />
          ))}
          {isLoading && (
            <div className="flex items-center gap-2 text-muted-foreground text-sm font-medium">
              <span className="w-2 h-2 bg-foreground rounded-full animate-bounce" />
              <span className="w-2 h-2 bg-foreground rounded-full animate-bounce [animation-delay:0.1s]" />
              <span className="w-2 h-2 bg-foreground rounded-full animate-bounce [animation-delay:0.2s]" />
            </div>
          )}
        </div>

        <ChatInput onSend={handleSendMessage} disabled={isLoading} />
      </Card>
    </main>
  );
}
