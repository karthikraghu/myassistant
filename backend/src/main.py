"""
Personal Assistant Agent - Entry Point
Run this file to start the agent.
"""

import os
import sys
from dotenv import load_dotenv

from core.agent import PersonalAssistantAgent
from utils.auth import authenticate_google

load_dotenv()


def main():
    """Main entry point for the personal assistant agent."""
    print("[INFO] Starting Personal Assistant Agent...")
    
    google_creds = authenticate_google()
    if not google_creds:
        print("[ERROR] Failed to authenticate with Google. Exiting.")
        sys.exit(1)
    
    print("[OK] Google authentication successful")
    
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("[ERROR] GEMINI_API_KEY not found in .env file. Exiting.")
        sys.exit(1)
    
    agent = PersonalAssistantAgent(
        gemini_api_key=gemini_api_key,
        google_creds=google_creds
    )
    
    print("[OK] Agent initialized")
    print("\n" + "="*50)
    print("Personal Executive Assistant Ready")
    print("Type 'quit' or 'exit' to stop.")
    print("="*50 + "\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ["quit", "exit"]:
                print("Goodbye.")
                break
            
            if not user_input:
                continue
            
            response = agent.process_request(user_input)
            print(f"\nAssistant: {response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye.")
            break


if __name__ == "__main__":
    main()
