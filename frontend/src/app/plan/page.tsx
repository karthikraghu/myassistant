"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import ChatInput from "@/components/ChatInput";
import ChatMessage from "@/components/ChatMessage";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft, RotateCcw, Sparkles } from "lucide-react";

interface Message {
    id: string;
    role: "user" | "assistant";
    content: string;
    timestamp: Date;
}

export default function PlanPage() {
    const router = useRouter();
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
        } catch {
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

    const handleReset = async () => {
        try {
            await fetch("/api/chat", { method: "DELETE" });
        } catch { /* ignore */ }
        setMessages([]);
    };

    return (
        <main className="min-h-screen flex flex-col p-4 md:p-6 max-w-3xl mx-auto fade-in">
            {/* Header */}
            <div className="flex items-center gap-3 mb-4">
                <Button
                    variant="outline"
                    size="icon"
                    onClick={() => router.push("/")}
                >
                    <ArrowLeft className="w-4 h-4" />
                </Button>

                <div className="flex-1">
                    <h1 className="text-xl font-black tracking-tight flex items-center gap-2">
                        <Sparkles className="w-5 h-5 text-accent" />
                        Plan My Day
                    </h1>
                    <p className="text-muted-foreground text-xs">Chat with J.A.R.V.I.S. to organize your schedule</p>
                </div>

                {messages.length > 0 && (
                    <Button
                        variant="ghost"
                        size="icon-sm"
                        onClick={handleReset}
                        title="Reset conversation"
                    >
                        <RotateCcw className="w-4 h-4" />
                    </Button>
                )}
            </div>

            {/* Chat Container */}
            <Card className="flex-1 flex flex-col border-[3px] border-foreground shadow-[4px_4px_0_var(--foreground)] overflow-hidden">
                {/* Messages */}
                <div className="flex-1 p-4 md:p-6 overflow-y-auto flex flex-col gap-4 min-h-[400px] max-h-[65vh] bg-background custom-scrollbar">
                    {messages.length === 0 && (
                        <div className="text-center text-muted-foreground m-auto p-6">
                            <Sparkles className="w-10 h-10 mx-auto mb-4 opacity-30" />
                            <p className="mb-4 font-bold text-sm">What do you want to plan?</p>
                            <ul className="space-y-2 max-w-xs mx-auto">
                                {[
                                    "Summarize my emails",
                                    "What's on my schedule today?",
                                    "Plan my day around my meetings",
                                    "Any urgent emails I should reply to?",
                                ].map((item) => (
                                    <li
                                        key={item}
                                        onClick={() => handleSendMessage(item)}
                                        className="p-3 bg-card border-2 border-foreground text-foreground text-sm cursor-pointer transition-all
                                            hover:bg-primary hover:text-primary-foreground
                                            hover:shadow-[2px_2px_0_var(--foreground)] hover:translate-x-[-2px] hover:translate-y-[-2px]
                                            active:translate-x-0 active:translate-y-0 active:shadow-none"
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
                            <span className="w-2 h-2 bg-primary rounded-full animate-bounce" />
                            <span className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:0.1s]" />
                            <span className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:0.2s]" />
                        </div>
                    )}
                </div>

                <ChatInput onSend={handleSendMessage} disabled={isLoading} />
            </Card>
        </main>
    );
}
