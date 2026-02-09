"""
Gmail Tools - Email-related tools for the agent.
"""

from langchain_core.tools import tool
from googleapiclient.errors import HttpError
import json

# Global service (set during initialization)
_gmail_service = None


def init_gmail_service(credentials):
    """Initialize Gmail API service with credentials."""
    global _gmail_service
    from googleapiclient.discovery import build
    _gmail_service = build("gmail", "v1", credentials=credentials)


@tool
def get_unread_emails(max_results: int = 10) -> str:
    """
    Fetch unread emails from the user's Gmail inbox.
    
    Args:
        max_results: Maximum number of emails to fetch (default 10)
        
    Returns:
        JSON string containing list of unread emails with sender, subject, and snippet
    """
    if not _gmail_service:
        return json.dumps({"error": "Gmail service not initialized"})
    
    try:
        results = _gmail_service.users().messages().list(
            userId="me",
            q="is:unread",
            maxResults=max_results
        ).execute()
        
        messages = results.get("messages", [])
        emails = []
        
        for msg in messages:
            message = _gmail_service.users().messages().get(
                userId="me",
                id=msg["id"],
                format="metadata",
                metadataHeaders=["From", "Subject", "Date"]
            ).execute()
            
            headers = message.get("payload", {}).get("headers", [])
            email_data = {
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
            
            emails.append(email_data)
        
        return json.dumps(emails, indent=2)
        
    except HttpError as error:
        return json.dumps({"error": str(error)})


@tool
def search_emails(query: str, max_results: int = 10) -> str:
    """
    Search emails with a Gmail query.
    
    Args:
        query: Gmail search query (e.g., "from:boss@company.com", "subject:urgent")
        max_results: Maximum number of results (default 10)
        
    Returns:
        JSON string containing matching emails
    """
    if not _gmail_service:
        return json.dumps({"error": "Gmail service not initialized"})
    
    try:
        results = _gmail_service.users().messages().list(
            userId="me",
            q=query,
            maxResults=max_results
        ).execute()
        
        messages = results.get("messages", [])
        emails = []
        
        for msg in messages:
            message = _gmail_service.users().messages().get(
                userId="me",
                id=msg["id"],
                format="metadata",
                metadataHeaders=["From", "Subject", "Date"]
            ).execute()
            
            headers = message.get("payload", {}).get("headers", [])
            email_data = {
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
            
            emails.append(email_data)
        
        return json.dumps(emails, indent=2)
        
    except HttpError as error:
        return json.dumps({"error": str(error)})
