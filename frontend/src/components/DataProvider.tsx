"use client";

import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from "react";

interface Email {
    snippet: string;
    from: string;
    subject: string;
    date: string;
}

interface CalendarEvent {
    summary: string;
    time: string;
    location: string;
    description?: string;
}

interface DataContextType {
    emails: Email[];
    events: CalendarEvent[];
    emailsLoading: boolean;
    eventsLoading: boolean;
    emailsError: string | null;
    eventsError: string | null;
    refreshEmails: () => Promise<void>;
    refreshEvents: () => Promise<void>;
}

const DataContext = createContext<DataContextType | null>(null);

export function useData() {
    const ctx = useContext(DataContext);
    if (!ctx) throw new Error("useData must be used inside DataProvider");
    return ctx;
}

export function DataProvider({ children }: { children: ReactNode }) {
    const [emails, setEmails] = useState<Email[]>([]);
    const [events, setEvents] = useState<CalendarEvent[]>([]);
    const [emailsLoading, setEmailsLoading] = useState(true);
    const [eventsLoading, setEventsLoading] = useState(true);
    const [emailsError, setEmailsError] = useState<string | null>(null);
    const [eventsError, setEventsError] = useState<string | null>(null);
    const [emailsFetched, setEmailsFetched] = useState(false);
    const [eventsFetched, setEventsFetched] = useState(false);

    const refreshEmails = useCallback(async () => {
        setEmailsLoading(true);
        setEmailsError(null);
        try {
            const res = await fetch("/api/emails");
            const data = await res.json();
            if (data.error) {
                setEmailsError(data.error);
            } else if (data.message) {
                setEmails([]);
            } else {
                setEmails(Array.isArray(data) ? data : []);
            }
        } catch {
            setEmailsError("Could not reach the server");
        } finally {
            setEmailsLoading(false);
            setEmailsFetched(true);
        }
    }, []);

    const refreshEvents = useCallback(async () => {
        setEventsLoading(true);
        setEventsError(null);
        try {
            const res = await fetch("/api/events");
            const data = await res.json();
            if (data.error) {
                setEventsError(data.error);
            } else if (data.message) {
                setEvents([]);
            } else {
                setEvents(Array.isArray(data) ? data : []);
            }
        } catch {
            setEventsError("Could not reach the server");
        } finally {
            setEventsLoading(false);
            setEventsFetched(true);
        }
    }, []);

    // Fetch only once on first mount — cached across navigations
    useEffect(() => {
        if (!emailsFetched) refreshEmails();
    }, [emailsFetched, refreshEmails]);

    useEffect(() => {
        if (!eventsFetched) refreshEvents();
    }, [eventsFetched, refreshEvents]);

    return (
        <DataContext.Provider value={{
            emails, events,
            emailsLoading, eventsLoading,
            emailsError, eventsError,
            refreshEmails, refreshEvents,
        }}>
            {children}
        </DataContext.Provider>
    );
}
