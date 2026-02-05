interface Message {
    id: string;
    role: "user" | "assistant";
    content: string;
    timestamp: Date;
}

interface ChatMessageProps {
    message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
    const isUser = message.role === "user";

    return (
        <div className={`flex flex-col gap-1 max-w-[80%] ${isUser ? "self-end" : "self-start"}`}>
            <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
                {isUser ? "You" : "Assistant"}
            </div>
            <div
                className={`p-3 border-[3px] border-foreground whitespace-pre-wrap ${isUser
                        ? "bg-primary text-primary-foreground shadow-[4px_4px_0_var(--foreground)]"
                        : "bg-card text-card-foreground shadow-[4px_4px_0_var(--foreground)]"
                    }`}
            >
                {message.content}
            </div>
        </div>
    );
}
