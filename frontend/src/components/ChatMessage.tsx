import styles from "./ChatMessage.module.css";

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
        <div className={`${styles.message} ${isUser ? styles.user : styles.assistant}`}>
            <div className={styles.label}>{isUser ? "You" : "J.A.R.V.I.S"}</div>
            <div className={styles.content}>{message.content}</div>
        </div>
    );
}
