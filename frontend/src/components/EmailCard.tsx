"use client";

import { Mail } from "lucide-react";

interface Email {
    snippet: string;
    from: string;
    subject: string;
    date: string;
}

interface EmailCardProps {
    email: Email;
    index: number;
}

function extractSenderName(from: string): string {
    // "John Doe <john@example.com>" → "John Doe"
    const match = from.match(/^(.+?)\s*<.*>$/);
    if (match) return match[1].replace(/"/g, "").trim();
    // "john@example.com" → "john"
    const emailMatch = from.match(/^([^@]+)@/);
    if (emailMatch) return emailMatch[1];
    return from;
}

function formatDate(dateStr: string): string {
    try {
        const date = new Date(dateStr);
        const now = new Date();
        const diffMs = now.getTime() - date.getTime();
        const diffHours = Math.floor(diffMs / (1000 * 60 * 60));

        if (diffHours < 1) return "Just now";
        if (diffHours < 24) return `${diffHours}h ago`;
        const diffDays = Math.floor(diffHours / 24);
        if (diffDays === 1) return "Yesterday";
        if (diffDays < 7) return `${diffDays}d ago`;
        return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
    } catch {
        return dateStr;
    }
}

export default function EmailCard({ email, index }: EmailCardProps) {
    const sender = extractSenderName(email.from);
    const initials = sender.slice(0, 2).toUpperCase();
    const timeAgo = formatDate(email.date);

    return (
        <div
            className={`group p-4 bg-card border-[3px] border-foreground transition-all cursor-pointer
                hover:bg-primary hover:text-primary-foreground
                hover:shadow-[4px_4px_0_var(--foreground)] hover:translate-x-[-2px] hover:translate-y-[-2px]
                active:translate-x-0 active:translate-y-0 active:shadow-none
                slide-up stagger-${Math.min(index + 1, 5)}`}
            style={{ animationFillMode: "backwards" }}
        >
            <div className="flex items-start gap-3">
                {/* Avatar */}
                <div className="shrink-0 w-9 h-9 bg-primary text-primary-foreground group-hover:bg-card group-hover:text-card-foreground border-2 border-foreground flex items-center justify-center text-xs font-bold uppercase">
                    {initials}
                </div>

                <div className="flex-1 min-w-0">
                    {/* Sender + Time */}
                    <div className="flex items-center justify-between gap-2 mb-1">
                        <span className="font-bold text-sm truncate">{sender}</span>
                        <span className="text-xs text-muted-foreground shrink-0 group-hover:text-primary-foreground/70">{timeAgo}</span>
                    </div>

                    {/* Subject */}
                    <p className="text-sm font-semibold truncate mb-1">{email.subject || "(No subject)"}</p>

                    {/* Snippet */}
                    <p className="text-xs text-muted-foreground line-clamp-2 leading-relaxed group-hover:text-primary-foreground/80">
                        {email.snippet}
                    </p>
                </div>

                {/* Mail icon */}
                <Mail className="w-4 h-4 shrink-0 mt-1 text-muted-foreground group-hover:text-primary-foreground/70" />
            </div>
        </div>
    );
}
