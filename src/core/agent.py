"""
Personal Assistant Agent - Core Agent Logic
Initializes the LLM and binds tools for execution.
"""

import google.generativeai as genai
from .prompts import SYSTEM_PROMPT, BRIEFING_PROMPT
from tools.gmail_tool import GmailTool
from tools.cal_tool import CalendarTool


class PersonalAssistantAgent:
    """Main agent class that orchestrates LLM and tools."""
    
    def __init__(self, gemini_api_key: str, google_creds):
        """
        Initialize the agent with API credentials.
        
        Args:
            gemini_api_key: Gemini API key for LLM access
            google_creds: Google OAuth credentials for Gmail/Calendar
        """
        # Configure Gemini
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-pro",
            system_instruction=SYSTEM_PROMPT
        )
        self.chat = self.model.start_chat(history=[])
        
        # Initialize tools
        self.gmail_tool = GmailTool(google_creds)
        self.calendar_tool = CalendarTool(google_creds)
    
    def process_request(self, user_input: str) -> str:
        """
        Process a user request and return a response.
        
        Args:
            user_input: Natural language request from the user
            
        Returns:
            Agent's response as a string
        """
        # Determine if we need to fetch data
        lower_input = user_input.lower()
        
        context_data = {}
        
        # Check if calendar data is needed
        if any(word in lower_input for word in ["calendar", "meeting", "schedule", "plan", "day", "tomorrow", "week"]):
            context_data["calendar_events"] = self.calendar_tool.get_today_events()
        
        # Check if email data is needed
        if any(word in lower_input for word in ["email", "mail", "inbox", "urgent", "plan", "day"]):
            context_data["unread_emails"] = self.gmail_tool.fetch_unread_emails()
        
        # Build the prompt with context
        if context_data:
            context_str = self._format_context(context_data)
            full_prompt = f"{user_input}\n\n## Context Data\n{context_str}"
        else:
            full_prompt = user_input
        
        # Get response from LLM
        response = self.chat.send_message(full_prompt)
        return response.text
    
    def _format_context(self, context_data: dict) -> str:
        """Format context data for the LLM prompt."""
        sections = []
        
        if "calendar_events" in context_data:
            events = context_data["calendar_events"]
            if events:
                events_str = "\n".join([f"- {e['time']}: {e['summary']}" for e in events])
            else:
                events_str = "No events scheduled"
            sections.append(f"### Calendar Events\n{events_str}")
        
        if "unread_emails" in context_data:
            emails = context_data["unread_emails"]
            if emails:
                emails_str = "\n".join([f"- From: {e['from']} | Subject: {e['subject']}" for e in emails])
            else:
                emails_str = "No unread emails"
            sections.append(f"### Unread Emails\n{emails_str}")
        
        return "\n\n".join(sections)
    
    def get_daily_briefing(self) -> str:
        """Generate a comprehensive daily briefing."""
        calendar_events = self.calendar_tool.get_today_events()
        unread_emails = self.gmail_tool.fetch_unread_emails()
        
        prompt = BRIEFING_PROMPT.format(
            calendar_events=calendar_events,
            unread_emails=unread_emails
        )
        
        response = self.chat.send_message(prompt)
        return response.text
