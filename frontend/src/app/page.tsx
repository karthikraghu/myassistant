"use client";

import { useRouter } from "next/navigation";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useData } from "@/components/DataProvider";
import EmailCard from "@/components/EmailCard";
import EventCard from "@/components/EventCard";
import { Mail, CalendarDays, ArrowRight, Sparkles, RefreshCw } from "lucide-react";

function SkeletonCard() {
  return (
    <div className="p-4 bg-card border-[3px] border-foreground/20 animate-pulse">
      <div className="flex items-start gap-3">
        <div className="w-9 h-9 bg-muted border-2 border-foreground/20" />
        <div className="flex-1 space-y-2">
          <div className="h-3 bg-muted w-2/3" />
          <div className="h-3 bg-muted w-full" />
          <div className="h-2 bg-muted w-4/5" />
        </div>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const router = useRouter();
  const {
    emails, events,
    emailsLoading, eventsLoading,
    emailsError, eventsError,
    refreshEmails, refreshEvents,
  } = useData();

  const now = new Date();
  const greeting = now.getHours() < 12 ? "Good morning" : now.getHours() < 17 ? "Good afternoon" : "Good evening";

  return (
    <main className="min-h-screen flex flex-col p-4 md:p-8 max-w-6xl mx-auto fade-in">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl md:text-4xl font-black tracking-tight">
              J.A.R.V.I.S.
            </h1>
            <p className="text-muted-foreground text-sm mt-1">
              {greeting}. Here&apos;s your day at a glance.
            </p>
          </div>
          <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-primary border-2 border-foreground text-primary-foreground text-xs font-bold uppercase shadow-[2px_2px_0_var(--foreground)]">
            <span className="w-2 h-2 bg-primary-foreground rounded-full animate-pulse" />
            Online
          </div>
        </div>

        {/* Plan My Day CTA */}
        <Button
          size="lg"
          onClick={() => router.push("/plan")}
          className="w-full md:w-auto gap-2"
        >
          <Sparkles className="w-4 h-4" />
          Plan My Day
          <ArrowRight className="w-4 h-4" />
        </Button>
      </div>

      {/* Dashboard Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 flex-1">
        {/* Email Section */}
        <section>
          <Card className="border-[3px] border-foreground shadow-[4px_4px_0_var(--foreground)] overflow-hidden">
            <div className="flex items-center justify-between p-4 border-b-[3px] border-foreground bg-card">
              <div className="flex items-center gap-2">
                <Mail className="w-5 h-5" />
                <h2 className="font-bold text-lg uppercase tracking-wide">Inbox</h2>
                {!emailsLoading && emails.length > 0 && (
                  <span className="px-2 py-0.5 bg-primary text-primary-foreground text-xs font-bold border-2 border-foreground">
                    {emails.length}
                  </span>
                )}
              </div>
              <button
                onClick={refreshEmails}
                disabled={emailsLoading}
                className="p-1.5 hover:bg-muted transition-colors disabled:opacity-50"
              >
                <RefreshCw className={`w-4 h-4 ${emailsLoading ? "animate-spin" : ""}`} />
              </button>
            </div>

            <div className="p-3 space-y-2 max-h-[60vh] overflow-y-auto custom-scrollbar">
              {emailsLoading && (
                <>
                  <SkeletonCard />
                  <SkeletonCard />
                  <SkeletonCard />
                </>
              )}

              {emailsError && (
                <div className="p-6 text-center text-muted-foreground">
                  <p className="text-sm">{emailsError}</p>
                  <button onClick={refreshEmails} className="text-primary text-sm mt-2 underline">
                    Retry
                  </button>
                </div>
              )}

              {!emailsLoading && !emailsError && emails.length === 0 && (
                <div className="p-8 text-center text-muted-foreground">
                  <Mail className="w-8 h-8 mx-auto mb-2 opacity-40" />
                  <p className="text-sm font-medium">Inbox zero — nice work</p>
                </div>
              )}

              {!emailsLoading && !emailsError && emails.map((email, i) => (
                <EmailCard key={`${email.subject}-${i}`} email={email} index={i} />
              ))}
            </div>
          </Card>
        </section>

        {/* Calendar Section */}
        <section>
          <Card className="border-[3px] border-foreground shadow-[4px_4px_0_var(--foreground)] overflow-hidden">
            <div className="flex items-center justify-between p-4 border-b-[3px] border-foreground bg-card">
              <div className="flex items-center gap-2">
                <CalendarDays className="w-5 h-5" />
                <h2 className="font-bold text-lg uppercase tracking-wide">Today</h2>
                {!eventsLoading && events.length > 0 && (
                  <span className="px-2 py-0.5 bg-accent text-accent-foreground text-xs font-bold border-2 border-foreground">
                    {events.length}
                  </span>
                )}
              </div>
              <button
                onClick={refreshEvents}
                disabled={eventsLoading}
                className="p-1.5 hover:bg-muted transition-colors disabled:opacity-50"
              >
                <RefreshCw className={`w-4 h-4 ${eventsLoading ? "animate-spin" : ""}`} />
              </button>
            </div>

            <div className="p-3 space-y-2 max-h-[60vh] overflow-y-auto custom-scrollbar">
              {eventsLoading && (
                <>
                  <SkeletonCard />
                  <SkeletonCard />
                </>
              )}

              {eventsError && (
                <div className="p-6 text-center text-muted-foreground">
                  <p className="text-sm">{eventsError}</p>
                  <button onClick={refreshEvents} className="text-primary text-sm mt-2 underline">
                    Retry
                  </button>
                </div>
              )}

              {!eventsLoading && !eventsError && events.length === 0 && (
                <div className="p-8 text-center text-muted-foreground">
                  <CalendarDays className="w-8 h-8 mx-auto mb-2 opacity-40" />
                  <p className="text-sm font-medium">No events today — you&apos;re free</p>
                </div>
              )}

              {!eventsLoading && !eventsError && events.map((event, i) => (
                <EventCard key={`${event.summary}-${i}`} event={event} index={i} />
              ))}
            </div>
          </Card>
        </section>
      </div>
    </main>
  );
}
