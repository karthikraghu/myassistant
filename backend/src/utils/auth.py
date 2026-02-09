"""
Google OAuth Authentication Handler.
Manages the OAuth2 flow for Gmail and Google Calendar access.
"""

import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes required for Gmail and Calendar read access
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly"
]

# Path to credentials files (in secrets folder)
PROJECT_ROOT = Path(__file__).parent.parent.parent
CREDENTIALS_FILE = PROJECT_ROOT / "secrets" / "credentials.json"
TOKEN_FILE = PROJECT_ROOT / "secrets" / "token.json"


def authenticate_google() -> Credentials | None:
    """
    Authenticate with Google OAuth2.
    
    This function handles the complete OAuth flow:
    1. Check for existing valid token
    2. Refresh expired token if possible
    3. Run OAuth flow if no valid credentials exist
    
    Returns:
        Google OAuth credentials or None if authentication fails
    """
    creds = None
    
    # Check for existing token
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception as e:
            print(f"[ERROR] Loading token: {e}")
            creds = None
    
    # If no valid credentials, refresh or get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print("[INFO] Refreshing expired token...")
                creds.refresh(Request())
            except Exception as e:
                print(f"[ERROR] Refreshing token: {e}")
                creds = None
        
        # If still no valid creds, run the OAuth flow
        if not creds:
            if not CREDENTIALS_FILE.exists():
                print(f"[ERROR] credentials.json not found at: {CREDENTIALS_FILE}")
                print("       Download it from Google Cloud Console.")
                return None
            
            print("[INFO] Starting OAuth flow...")
            print("       A browser window will open for authentication.")
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_FILE),
                    SCOPES
                )
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"[ERROR] OAuth flow failed: {e}")
                return None
        
        # Save the credentials for next run
        if creds:
            try:
                # Ensure secrets directory exists
                TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
                with open(TOKEN_FILE, "w") as token:
                    token.write(creds.to_json())
                print(f"[OK] Token saved to: {TOKEN_FILE}")
            except Exception as e:
                print(f"[WARN] Could not save token: {e}")
    
    return creds


def revoke_credentials():
    """
    Revoke stored credentials and delete token file.
    Use this when you want to re-authenticate with different permissions.
    """
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
            
            import requests
            requests.post(
                "https://oauth2.googleapis.com/revoke",
                params={"token": creds.token},
                headers={"content-type": "application/x-www-form-urlencoded"}
            )
            
            TOKEN_FILE.unlink()
            print("[OK] Credentials revoked and token deleted")
            
        except Exception as e:
            print(f"[ERROR] Revoking credentials: {e}")
            try:
                TOKEN_FILE.unlink()
            except:
                pass
    else:
        print("[INFO] No token file found")


if __name__ == "__main__":
    print("[INFO] Testing Google Authentication...")
    creds = authenticate_google()
    
    if creds:
        print("[OK] Authentication successful")
        print(f"     Token expires: {creds.expiry}")
    else:
        print("[ERROR] Authentication failed")
