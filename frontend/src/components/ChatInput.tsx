"use client";

import { useState, KeyboardEvent } from "react";
import styles from "./ChatInput.module.css";

interface ChatInputProps {
    onSend: (message: string) => void;
    disabled?: boolean;
}

export default function ChatInput({ onSend, disabled }: ChatInputProps) {
    const [input, setInput] = useState("");

    const handleSubmit = () => {
        if (input.trim() && !disabled) {
            onSend(input.trim());
            setInput("");
        }
    };

    const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    return (
        <div className={styles.container}>
            <textarea
                className={styles.input}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="What can I help you with today, sir?"
                disabled={disabled}
                rows={1}
            />
            <button
                className={styles.button}
                onClick={handleSubmit}
                disabled={disabled || !input.trim()}
            >
                Execute
            </button>
        </div>
    );
}
