"""
Chat manager for integrating GUI with AI module.
"""

import logging
from typing import List, Optional, Dict, Any

# Import AI module
from ai.ai_manager import AIManager
from ai.chat_memory import ChatMessage, MessageRole

logger = logging.getLogger(__name__)


class ChatManager:
    """Manages chat interactions with the AI."""
    
    def __init__(self):
        """Initialize the chat manager."""
        self.ai_manager = AIManager()
        self.current_session_id = None
    
    def startNewSession(self) -> str:
        """Start a new chat session."""
        try:
            session = self.ai_manager.create_chat_session()
            self.current_session_id = session.session_id
            logger.info(f"Started new chat session: {self.current_session_id}")
            return self.current_session_id
        except Exception as e:
            logger.error(f"Failed to start new session: {e}")
            return None
    
    def sendMessage(self, message: str) -> Optional[str]:
        """Send a message to the AI and get response."""
        try:
            if not self.current_session_id:
                self.startNewSession()
            
            # Add user message
            self.ai_manager.memory_manager.add_message(
                self.current_session_id, 
                MessageRole.USER.value, 
                message
            )
            
            # Get AI response using chat method
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                response = loop.run_until_complete(self.ai_manager.chat(message))
            finally:
                loop.close()
            
            if response:
                # Add AI response to memory
                self.ai_manager.memory_manager.add_message(
                    self.current_session_id, 
                    MessageRole.ASSISTANT.value, 
                    response
                )
                
                logger.info(f"AI response generated for session {self.current_session_id}")
                return response
            else:
                logger.error("Failed to generate AI response")
                return "Sorry, I couldn't generate a response. Please try again."
                
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return f"Error: {e}"
    
    def getChatHistory(self) -> List[Dict[str, Any]]:
        """Get chat history for the current session."""
        if not self.current_session_id:
            return []
        
        try:
            session = self.ai_manager.memory_manager.get_session(self.current_session_id)
            if not session:
                return []
            
            history = []
            for message in session.messages:
                history.append({
                    'role': message.role,
                    'content': message.content,
                    'timestamp': message.timestamp.isoformat() if message.timestamp else None
                })
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting chat history: {e}")
            return []
    
    def clearChatHistory(self):
        """Clear chat history for the current session."""
        if self.current_session_id:
            try:
                # Clear messages in the session
                session = self.ai_manager.memory_manager.get_session(self.current_session_id)
                if session:
                    session.messages.clear()
                logger.info(f"Cleared chat history for session {self.current_session_id}")
            except Exception as e:
                logger.error(f"Error clearing chat history: {e}")
    
    def endSession(self):
        """End the current chat session."""
        if self.current_session_id:
            try:
                self.ai_manager.end_session(self.current_session_id)
                logger.info(f"Ended chat session {self.current_session_id}")
                self.current_session_id = None
            except Exception as e:
                logger.error(f"Error ending session: {e}")
    
    def getCurrentSessionId(self) -> Optional[str]:
        """Get the current session ID."""
        return self.current_session_id
    
    def isSessionActive(self) -> bool:
        """Check if there's an active session."""
        return self.current_session_id is not None