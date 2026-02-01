"""
Gmail Tool - Functions to fetch and parse emails from Gmail API.
"""

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText


class GmailTool:
    """Tool for interacting with Gmail API."""
    
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
    
    def __init__(self, credentials):
        """
        Initialize Gmail tool with credentials.
        
        Args:
            credentials: Google OAuth credentials
        """
        self.service = build("gmail", "v1", credentials=credentials)
    
    def fetch_unread_emails(self, max_results: int = 10) -> list[dict]:
        """
        Fetch unread emails from the user's inbox.
        
        Args:
            max_results: Maximum number of emails to fetch
            
        Returns:
            List of email dictionaries with 'from', 'subject', 'snippet', 'date'
        """
        try:
            results = self.service.users().messages().list(
                userId="me",
                q="is:unread",
                maxResults=max_results
            ).execute()
            
            messages = results.get("messages", [])
            emails = []
            
            for msg in messages:
                email_data = self._get_email_details(msg["id"])
                if email_data:
                    emails.append(email_data)
            
            return emails
            
        except HttpError as error:
            print(f"Gmail API error: {error}")
            return []
    
    def _get_email_details(self, message_id: str) -> dict | None:
        """
        Get detailed information about a specific email.
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            Dictionary with email details or None if error
        """
        try:
            message = self.service.users().messages().get(
                userId="me",
                id=message_id,
                format="metadata",
                metadataHeaders=["From", "Subject", "Date"]
            ).execute()
            
            headers = message.get("payload", {}).get("headers", [])
            email_data = {
                "id": message_id,
                "snippet": message.get("snippet", ""),
                "from": "",
                "subject": "",
                "date": ""
            }
            
            for header in headers:
                name = header.get("name", "").lower()
                value = header.get("value", "")
                
                if name == "from":
                    email_data["from"] = value
                elif name == "subject":
                    email_data["subject"] = value
                elif name == "date":
                    email_data["date"] = value
            
            return email_data
            
        except HttpError as error:
            print(f"Error fetching email {message_id}: {error}")
            return None
    
    def search_emails(self, query: str, max_results: int = 10) -> list[dict]:
        """
        Search emails with a custom query.
        
        Args:
            query: Gmail search query (e.g., "from:boss@company.com")
            max_results: Maximum number of results
            
        Returns:
            List of matching email dictionaries
        """
        try:
            results = self.service.users().messages().list(
                userId="me",
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get("messages", [])
            emails = []
            
            for msg in messages:
                email_data = self._get_email_details(msg["id"])
                if email_data:
                    emails.append(email_data)
            
            return emails
            
        except HttpError as error:
            print(f"Gmail search error: {error}")
            return []
