"""
Chat Memory Management for TarotMac AI Module

This module provides conversation memory management, context tracking,
and integration with the database for persistent chat history.
"""

import json
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import uuid
import logging

logger = logging.getLogger(__name__)


class MessageRole(Enum):
    """Enumeration of message roles in chat."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class ChatMessage:
    """Represents a single chat message."""
    
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    role: str = "user"  # "user", "assistant", "system"
    content: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization."""
        return {
            "message_id": self.message_id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatMessage':
        """Create message from dictionary."""
        return cls(
            message_id=data.get("message_id", str(uuid.uuid4())),
            role=data.get("role", "user"),
            content=data.get("content", ""),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            metadata=data.get("metadata", {})
        )


@dataclass
class ChatSession:
    """Represents a chat session with memory and context."""
    
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    messages: List[ChatMessage] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = True
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> ChatMessage:
        """Add a message to the session."""
        message = ChatMessage(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        self.messages.append(message)
        self.last_activity = datetime.now()
        return message
    
    def get_recent_messages(self, count: int = 10) -> List[ChatMessage]:
        """Get the most recent messages."""
        return self.messages[-count:] if self.messages else []
    
    def get_messages_for_llm(self, max_tokens: int = 4000) -> List[Dict[str, str]]:
        """Get messages formatted for LLM consumption with token limit."""
        messages = []
        current_tokens = 0
        
        # Start from most recent and work backwards
        for message in reversed(self.messages):
            message_tokens = len(message.content.split()) * 1.3  # Rough token estimate
            if current_tokens + message_tokens > max_tokens:
                break
            
            messages.insert(0, {
                "role": message.role,
                "content": message.content
            })
            current_tokens += message_tokens
        
        return messages
    
    def clear_old_messages(self, keep_recent: int = 20) -> int:
        """Clear old messages, keeping only the most recent ones."""
        if len(self.messages) <= keep_recent:
            return 0
        
        removed_count = len(self.messages) - keep_recent
        self.messages = self.messages[-keep_recent:]
        return removed_count
    
    def update_context(self, key: str, value: Any) -> None:
        """Update session context."""
        self.context[key] = value
        self.last_activity = datetime.now()
    
    def get_context_summary(self) -> str:
        """Get a summary of the session context."""
        if not self.context:
            return "No specific context"
        
        summary_parts = []
        if 'reading' in self.context:
            reading = self.context['reading']
            summary_parts.append(f"Reading: {reading.get('title', 'Untitled')}")
        
        if 'card' in self.context:
            card = self.context['card']
            summary_parts.append(f"Card: {card.get('name', 'Unknown')}")
        
        if 'topic' in self.context:
            summary_parts.append(f"Topic: {self.context['topic']}")
        
        return "; ".join(summary_parts) if summary_parts else "General conversation"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "title": self.title,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "messages": [msg.to_dict() for msg in self.messages],
            "context": self.context,
            "is_active": self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatSession':
        """Create session from dictionary."""
        return cls(
            session_id=data.get("session_id", str(uuid.uuid4())),
            title=data.get("title", ""),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            last_activity=datetime.fromisoformat(data.get("last_activity", datetime.now().isoformat())),
            messages=[ChatMessage.from_dict(msg_data) for msg_data in data.get("messages", [])],
            context=data.get("context", {}),
            is_active=data.get("is_active", True)
        )


class ChatMemoryManager:
    """Manages chat sessions and memory for the AI module."""
    
    def __init__(self, max_sessions: int = 50, max_session_age_days: int = 30):
        """
        Initialize the chat memory manager.
        
        Args:
            max_sessions: Maximum number of sessions to keep in memory
            max_session_age_days: Maximum age of sessions before cleanup
        """
        self.max_sessions = max_sessions
        self.max_session_age_days = max_session_age_days
        self.sessions: Dict[str, ChatSession] = {}
        self.current_session_id: Optional[str] = None
    
    def create_session(self, title: str = "", context: Optional[Dict[str, Any]] = None) -> ChatSession:
        """Create a new chat session."""
        session = ChatSession(
            title=title or f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            context=context or {}
        )
        self.sessions[session.session_id] = session
        self.current_session_id = session.session_id
        
        # Cleanup old sessions if needed
        self._cleanup_old_sessions()
        
        return session
    
    def get_current_session(self) -> Optional[ChatSession]:
        """Get the current active session."""
        if self.current_session_id and self.current_session_id in self.sessions:
            return self.sessions[self.current_session_id]
        return None
    
    def set_current_session(self, session_id: str) -> bool:
        """Set the current session by ID."""
        if session_id in self.sessions:
            self.current_session_id = session_id
            return True
        return False
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a session by ID."""
        return self.sessions.get(session_id)
    
    def list_sessions(self, include_inactive: bool = False) -> List[ChatSession]:
        """List all sessions, optionally including inactive ones."""
        sessions = list(self.sessions.values())
        
        if not include_inactive:
            sessions = [s for s in sessions if s.is_active]
        
        # Sort by last activity, most recent first
        return sorted(sessions, key=lambda s: s.last_activity, reverse=True)
    
    def add_message(self, role: str, content: str, 
                   session_id: Optional[str] = None,
                   metadata: Optional[Dict[str, Any]] = None) -> Optional[ChatMessage]:
        """Add a message to a session."""
        target_session_id = session_id or self.current_session_id
        
        if not target_session_id or target_session_id not in self.sessions:
            return None
        
        session = self.sessions[target_session_id]
        return session.add_message(role, content, metadata)
    
    def get_conversation_context(self, session_id: Optional[str] = None,
                               max_tokens: int = 4000) -> Tuple[List[Dict[str, str]], Dict[str, Any]]:
        """Get conversation context for LLM."""
        target_session_id = session_id or self.current_session_id
        
        if not target_session_id or target_session_id not in self.sessions:
            return [], {}
        
        session = self.sessions[target_session_id]
        messages = session.get_messages_for_llm(max_tokens)
        context = session.context.copy()
        
        return messages, context
    
    def update_session_context(self, key: str, value: Any, 
                             session_id: Optional[str] = None) -> bool:
        """Update session context."""
        target_session_id = session_id or self.current_session_id
        
        if not target_session_id or target_session_id not in self.sessions:
            return False
        
        self.sessions[target_session_id].update_context(key, value)
        return True
    
    def end_session(self, session_id: Optional[str] = None) -> bool:
        """End a session."""
        target_session_id = session_id or self.current_session_id
        
        if not target_session_id or target_session_id not in self.sessions:
            return False
        
        self.sessions[target_session_id].is_active = False
        
        if target_session_id == self.current_session_id:
            self.current_session_id = None
        
        return True
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session completely."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            
            if session_id == self.current_session_id:
                self.current_session_id = None
            
            return True
        return False
    
    def cleanup_old_messages(self, session_id: Optional[str] = None,
                           keep_recent: int = 20) -> int:
        """Cleanup old messages in sessions."""
        if session_id:
            if session_id in self.sessions:
                return self.sessions[session_id].clear_old_messages(keep_recent)
            return 0
        
        total_removed = 0
        for session in self.sessions.values():
            total_removed += session.clear_old_messages(keep_recent)
        
        return total_removed
    
    def _cleanup_old_sessions(self) -> None:
        """Cleanup old sessions based on age and count limits."""
        now = datetime.now()
        cutoff_date = now - timedelta(days=self.max_session_age_days)
        
        # Remove sessions older than cutoff date
        sessions_to_remove = []
        for session_id, session in self.sessions.items():
            if session.last_activity < cutoff_date:
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            del self.sessions[session_id]
        
        # If still too many sessions, remove oldest inactive ones
        if len(self.sessions) > self.max_sessions:
            inactive_sessions = [
                (session_id, session) for session_id, session in self.sessions.items()
                if not session.is_active
            ]
            
            # Sort by last activity, oldest first
            inactive_sessions.sort(key=lambda x: x[1].last_activity)
            
            # Remove oldest inactive sessions
            excess_count = len(self.sessions) - self.max_sessions
            for i in range(min(excess_count, len(inactive_sessions))):
                session_id = inactive_sessions[i][0]
                del self.sessions[session_id]
    
    def export_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Export a session for backup or sharing."""
        if session_id in self.sessions:
            return self.sessions[session_id].to_dict()
        return None
    
    def import_session(self, session_data: Dict[str, Any]) -> Optional[ChatSession]:
        """Import a session from backup data."""
        try:
            session = ChatSession.from_dict(session_data)
            self.sessions[session.session_id] = session
            return session
        except Exception as e:
            logger.error(f"Error importing session: {e}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get memory manager statistics."""
        total_sessions = len(self.sessions)
        active_sessions = sum(1 for s in self.sessions.values() if s.is_active)
        total_messages = sum(len(s.messages) for s in self.sessions.values())
        
        return {
            "total_sessions": total_sessions,
            "active_sessions": active_sessions,
            "total_messages": total_messages,
            "current_session_id": self.current_session_id,
            "max_sessions": self.max_sessions,
            "max_session_age_days": self.max_session_age_days
        }