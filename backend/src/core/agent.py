"""
Personal Assistant Agent - LangChain ReAct Agent
Uses LangGraph for agent control flow with Gmail and Calendar tools.
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from tools import get_all_tools, init_google_services
from .prompts import SYSTEM_PROMPT


class PersonalAssistantAgent:
    """LangChain-powered personal assistant agent."""
    
    def __init__(self, gemini_api_key: str, google_creds):
        """
        Initialize the agent with credentials.
        
        Args:
            gemini_api_key: Gemini API key
            google_creds: Google OAuth credentials for Gmail/Calendar
        """
        # Initialize Google services for tools
        init_google_services(google_creds)
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=gemini_api_key,
            temperature=0.3
        )
        
        # Get LangChain tools
        self.tools = get_all_tools()
        
        # Create memory for conversation history
        self.memory = MemorySaver()
        
        # Create ReAct agent with LangGraph (simple config)
        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            checkpointer=self.memory
        )
        
        # Session config for memory
        self.config = {"configurable": {"thread_id": "default"}}
        
        # Store system prompt
        self.system_prompt = SYSTEM_PROMPT
    
    def process_request(self, user_input: str) -> str:
        """
        Process a user request using the ReAct agent.
        
        Args:
            user_input: Natural language request
            
        Returns:
            Agent's response as a string
        """
        try:
            # Include system instructions with user message
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=user_input)
            ]
            
            response = self.agent.invoke(
                {"messages": messages},
                config=self.config
            )
            
            # Extract the final AI message
            result_messages = response.get("messages", [])
            if result_messages:
                # Find the last AI message (not tool messages)
                for msg in reversed(result_messages):
                    if hasattr(msg, 'content') and msg.content:
                        # Check if it's an AI message
                        if isinstance(msg, AIMessage):
                            content = msg.content
                            if isinstance(content, str) and content.strip():
                                return content
                            elif isinstance(content, list):
                                # Handle structured content
                                text_parts = [p.get('text', '') for p in content if isinstance(p, dict) and 'text' in p]
                                if text_parts:
                                    return ' '.join(text_parts)
                
                # Fallback: return last message content
                last_msg = result_messages[-1]
                if hasattr(last_msg, 'content') and last_msg.content:
                    content = last_msg.content
                    if isinstance(content, str):
                        return content
                    return str(content)
            
            return "I couldn't process your request."
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"Error processing request: {str(e)}"
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.config = {"configurable": {"thread_id": f"session_{os.urandom(4).hex()}"}}
