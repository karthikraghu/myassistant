"""
Calendar Tool - Functions to fetch and parse events from Google Calendar API.
"""

from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class CalendarTool:
    """Tool for interacting with Google Calendar API."""
    
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    
    def __init__(self, credentials):
        """
        Initialize Calendar tool with credentials.
        
        Args:
            credentials: Google OAuth credentials
        """
        self.service = build("calendar", "v3", credentials=credentials)
    
    def get_today_events(self) -> list[dict]:
        """
        Get all events for today.
        
        Returns:
            List of event dictionaries with 'summary', 'time', 'location', 'description'
        """
        now = datetime.utcnow()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        return self.get_events_in_range(
            start_of_day.isoformat() + "Z",
            end_of_day.isoformat() + "Z"
        )
    
    def get_tomorrow_events(self) -> list[dict]:
        """
        Get all events for tomorrow.
        
        Returns:
            List of event dictionaries
        """
        now = datetime.utcnow()
        start_of_tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_tomorrow = start_of_tomorrow + timedelta(days=1)
        
        return self.get_events_in_range(
            start_of_tomorrow.isoformat() + "Z",
            end_of_tomorrow.isoformat() + "Z"
        )
    
    def get_week_events(self) -> list[dict]:
        """
        Get all events for the next 7 days.
        
        Returns:
            List of event dictionaries
        """
        now = datetime.utcnow()
        end_of_week = now + timedelta(days=7)
        
        return self.get_events_in_range(
            now.isoformat() + "Z",
            end_of_week.isoformat() + "Z"
        )
    
    def get_events_in_range(self, time_min: str, time_max: str) -> list[dict]:
        """
        Get events within a specific time range.
        
        Args:
            time_min: Start time in RFC3339 format
            time_max: End time in RFC3339 format
            
        Returns:
            List of event dictionaries
        """
        try:
            events_result = self.service.events().list(
                calendarId="primary",
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy="startTime"
            ).execute()
            
            events = events_result.get("items", [])
            
            return [self._parse_event(event) for event in events]
            
        except HttpError as error:
            print(f"Calendar API error: {error}")
            return []
    
    def _parse_event(self, event: dict) -> dict:
        """
        Parse a raw calendar event into a structured format.
        
        Args:
            event: Raw event from Google Calendar API
            
        Returns:
            Parsed event dictionary
        """
        start = event.get("start", {})
        start_time = start.get("dateTime", start.get("date", ""))
        
        # Format the time for display
        if "dateTime" in start:
            dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            formatted_time = dt.strftime("%I:%M %p")
        else:
            formatted_time = "All day"
        
        end = event.get("end", {})
        end_time = end.get("dateTime", end.get("date", ""))
        
        return {
            "id": event.get("id", ""),
            "summary": event.get("summary", "No title"),
            "time": formatted_time,
            "start": start_time,
            "end": end_time,
            "location": event.get("location", ""),
            "description": event.get("description", ""),
            "attendees": [a.get("email", "") for a in event.get("attendees", [])]
        }
    
    def find_free_slots(self, date: datetime = None, min_duration_minutes: int = 30) -> list[dict]:
        """
        Find free time slots in the calendar.
        
        Args:
            date: Date to check (defaults to today)
            min_duration_minutes: Minimum slot duration to consider
            
        Returns:
            List of free slot dictionaries with 'start' and 'end' times
        """
        if date is None:
            date = datetime.utcnow()
        
        # Get events for the day
        start_of_day = date.replace(hour=9, minute=0, second=0, microsecond=0)  # Work hours start
        end_of_day = date.replace(hour=18, minute=0, second=0, microsecond=0)   # Work hours end
        
        events = self.get_events_in_range(
            start_of_day.isoformat() + "Z",
            end_of_day.isoformat() + "Z"
        )
        
        # Find gaps between events
        free_slots = []
        current_time = start_of_day
        
        for event in events:
            event_start = datetime.fromisoformat(event["start"].replace("Z", "+00:00"))
            event_end = datetime.fromisoformat(event["end"].replace("Z", "+00:00"))
            
            # Check if there's a gap before this event
            gap_minutes = (event_start - current_time).total_seconds() / 60
            if gap_minutes >= min_duration_minutes:
                free_slots.append({
                    "start": current_time.isoformat(),
                    "end": event_start.isoformat(),
                    "duration_minutes": int(gap_minutes)
                })
            
            current_time = max(current_time, event_end)
        
        # Check for free time after the last event
        gap_minutes = (end_of_day - current_time).total_seconds() / 60
        if gap_minutes >= min_duration_minutes:
            free_slots.append({
                "start": current_time.isoformat(),
                "end": end_of_day.isoformat(),
                "duration_minutes": int(gap_minutes)
            })
        
        return free_slots
