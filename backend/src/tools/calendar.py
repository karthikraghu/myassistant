"""
Calendar Tools - Google Calendar tools for the agent.
"""

from langchain_core.tools import tool
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import json

# Global service (set during initialization)
_calendar_service = None


def init_calendar_service(credentials):
    """Initialize Google Calendar API service with credentials."""
    global _calendar_service
    from googleapiclient.discovery import build
    _calendar_service = build("calendar", "v3", credentials=credentials)


@tool
def get_today_events() -> str:
    """
    Get all calendar events for today.
    
    Returns:
        JSON string containing today's events with time, summary, and location
    """
    if not _calendar_service:
        return json.dumps({"error": "Calendar service not initialized"})
    
    try:
        now = datetime.utcnow()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        events_result = _calendar_service.events().list(
            calendarId="primary",
            timeMin=start_of_day.isoformat() + "Z",
            timeMax=end_of_day.isoformat() + "Z",
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        
        events = events_result.get("items", [])
        parsed_events = []
        
        for event in events:
            start = event.get("start", {})
            start_time = start.get("dateTime", start.get("date", ""))
            
            if "dateTime" in start:
                dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                formatted_time = dt.strftime("%I:%M %p")
            else:
                formatted_time = "All day"
            
            parsed_events.append({
                "summary": event.get("summary", "No title"),
                "time": formatted_time,
                "location": event.get("location", ""),
                "description": event.get("description", "")
            })
        
        if not parsed_events:
            return json.dumps({"message": "No events scheduled for today"})
        
        return json.dumps(parsed_events, indent=2)
        
    except HttpError as error:
        return json.dumps({"error": str(error)})


@tool
def get_week_events() -> str:
    """
    Get all calendar events for the next 7 days.
    
    Returns:
        JSON string containing this week's events
    """
    if not _calendar_service:
        return json.dumps({"error": "Calendar service not initialized"})
    
    try:
        now = datetime.utcnow()
        end_of_week = now + timedelta(days=7)
        
        events_result = _calendar_service.events().list(
            calendarId="primary",
            timeMin=now.isoformat() + "Z",
            timeMax=end_of_week.isoformat() + "Z",
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        
        events = events_result.get("items", [])
        parsed_events = []
        
        for event in events:
            start = event.get("start", {})
            start_time = start.get("dateTime", start.get("date", ""))
            
            if "dateTime" in start:
                dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                formatted_time = dt.strftime("%a %b %d, %I:%M %p")
            else:
                formatted_time = start_time + " (All day)"
            
            parsed_events.append({
                "summary": event.get("summary", "No title"),
                "time": formatted_time,
                "location": event.get("location", "")
            })
        
        if not parsed_events:
            return json.dumps({"message": "No events scheduled for this week"})
        
        return json.dumps(parsed_events, indent=2)
        
    except HttpError as error:
        return json.dumps({"error": str(error)})


@tool
def get_tomorrow_events() -> str:
    """
    Get all calendar events for tomorrow.
    
    Returns:
        JSON string containing tomorrow's events
    """
    if not _calendar_service:
        return json.dumps({"error": "Calendar service not initialized"})
    
    try:
        now = datetime.utcnow()
        start_of_tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_tomorrow = start_of_tomorrow + timedelta(days=1)
        
        events_result = _calendar_service.events().list(
            calendarId="primary",
            timeMin=start_of_tomorrow.isoformat() + "Z",
            timeMax=end_of_tomorrow.isoformat() + "Z",
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        
        events = events_result.get("items", [])
        parsed_events = []
        
        for event in events:
            start = event.get("start", {})
            start_time = start.get("dateTime", start.get("date", ""))
            
            if "dateTime" in start:
                dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                formatted_time = dt.strftime("%I:%M %p")
            else:
                formatted_time = "All day"
            
            parsed_events.append({
                "summary": event.get("summary", "No title"),
                "time": formatted_time,
                "location": event.get("location", "")
            })
        
        if not parsed_events:
            return json.dumps({"message": "No events scheduled for tomorrow"})
        
        return json.dumps(parsed_events, indent=2)
        
    except HttpError as error:
        return json.dumps({"error": str(error)})
