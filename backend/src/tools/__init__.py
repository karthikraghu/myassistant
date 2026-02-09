"""
Tools Package - Clean exports for all LangChain tools.
"""

from .gmail import get_unread_emails, search_emails, init_gmail_service
from .calendar import get_today_events, get_week_events, get_tomorrow_events, init_calendar_service


def init_google_services(credentials):
    """Initialize all Google API services with credentials."""
    init_gmail_service(credentials)
    init_calendar_service(credentials)


def get_all_tools():
    """Return all available LangChain tools."""
    return [
        # Gmail tools
        get_unread_emails,
        search_emails,
        # Calendar tools
        get_today_events,
        get_week_events,
        get_tomorrow_events
    ]


# Clean exports
__all__ = [
    # Initialization
    "init_google_services",
    "get_all_tools",
    # Gmail
    "get_unread_emails",
    "search_emails",
    # Calendar
    "get_today_events",
    "get_week_events",
    "get_tomorrow_events"
]
