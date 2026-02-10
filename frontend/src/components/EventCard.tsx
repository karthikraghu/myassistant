"use client";

import { Clock, MapPin, CalendarDays } from "lucide-react";

interface CalendarEvent {
    summary: string;
    time: string;
    location: string;
    description?: string;
}

interface EventCardProps {
    event: CalendarEvent;
    index: number;
}

export default function EventCard({ event, index }: EventCardProps) {
    const isAllDay = event.time === "All day";

    return (
        <div
            className={`group p-4 bg-card border-[3px] border-foreground transition-all cursor-pointer
                hover:bg-accent hover:text-accent-foreground
                hover:shadow-[4px_4px_0_var(--foreground)] hover:translate-x-[-2px] hover:translate-y-[-2px]
                active:translate-x-0 active:translate-y-0 active:shadow-none
                slide-up stagger-${Math.min(index + 1, 5)}`}
            style={{ animationFillMode: "backwards" }}
        >
            <div className="flex items-start gap-3">
                {/* Time badge */}
                <div className={`shrink-0 px-2 py-1 border-2 border-foreground text-xs font-bold uppercase text-center min-w-[60px] ${isAllDay
                        ? "bg-secondary text-secondary-foreground"
                        : "bg-primary text-primary-foreground"
                    }`}>
                    {isAllDay ? "ALL DAY" : event.time}
                </div>

                <div className="flex-1 min-w-0">
                    {/* Event title */}
                    <p className="font-bold text-sm mb-1">{event.summary}</p>

                    {/* Location */}
                    {event.location && (
                        <div className="flex items-center gap-1 text-xs text-muted-foreground group-hover:text-accent-foreground/70">
                            <MapPin className="w-3 h-3" />
                            <span className="truncate">{event.location}</span>
                        </div>
                    )}

                    {/* Description preview */}
                    {event.description && (
                        <p className="text-xs text-muted-foreground mt-1 line-clamp-1 group-hover:text-accent-foreground/70">
                            {event.description}
                        </p>
                    )}
                </div>

                <CalendarDays className="w-4 h-4 shrink-0 mt-1 text-muted-foreground group-hover:text-accent-foreground/70" />
            </div>
        </div>
    );
}
