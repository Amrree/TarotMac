"""
SQLAlchemy models for the Tarot application database.
"""

from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()


class Card(Base):
    """Individual tarot card with all metadata."""
    
    __tablename__ = 'cards'
    
    id = Column(String, primary_key=True)  # e.g., 'fool', 'ace_wands'
    name = Column(String, nullable=False)
    arcana = Column(String, nullable=False)  # 'major' or 'minor'
    suit = Column(String, nullable=True)  # 'wands', 'cups', 'swords', 'pentacles'
    number = Column(Integer, nullable=True)  # 0-21 for major, 1-10 for minor
    rank = Column(String, nullable=True)  # 'page', 'knight', 'queen', 'king' for court cards
    element = Column(String, nullable=False)
    keywords = Column(JSON, nullable=False)  # List of keywords
    upright_text = Column(Text, nullable=False)
    reversed_text = Column(Text, nullable=False)
    polarity_baseline = Column(Float, nullable=False)  # -2 to +2
    intensity_baseline = Column(Float, nullable=False)  # 0 to 1
    themes = Column(JSON, nullable=False)  # Dict of theme weights
    
    # Relationships
    reading_positions = relationship("ReadingPosition", back_populates="card")


class Spread(Base):
    """Tarot spread definitions."""
    
    __tablename__ = 'spreads'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    positions = Column(JSON, nullable=False)  # List of position definitions
    is_custom = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    readings = relationship("Reading", back_populates="spread")


class Reading(Base):
    """Individual tarot reading session."""
    
    __tablename__ = 'readings'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    spread_id = Column(String, ForeignKey('spreads.id'), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    tags = Column(JSON, nullable=True)  # List of tags
    people_names = Column(JSON, nullable=True)  # List of people mentioned
    location = Column(String, nullable=True)
    is_private = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    
    # Relationships
    spread = relationship("Spread", back_populates="readings")
    positions = relationship("ReadingPosition", back_populates="reading", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="reading")


class ReadingPosition(Base):
    """Individual card position within a reading."""
    
    __tablename__ = 'reading_positions'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    reading_id = Column(String, ForeignKey('readings.id'), nullable=False)
    card_id = Column(String, ForeignKey('cards.id'), nullable=False)
    position_name = Column(String, nullable=False)  # e.g., 'past', 'present', 'future'
    position_index = Column(Integer, nullable=False)  # Order in spread
    orientation = Column(String, nullable=False)  # 'upright' or 'reversed'
    x_coordinate = Column(Float, nullable=True)  # For custom layouts
    y_coordinate = Column(Float, nullable=True)  # For custom layouts
    
    # Relationships
    reading = relationship("Reading", back_populates="positions")
    card = relationship("Card", back_populates="reading_positions")


class Conversation(Base):
    """AI conversation linked to a reading or standalone."""
    
    __tablename__ = 'conversations'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    reading_id = Column(String, ForeignKey('readings.id'), nullable=True)  # Null for standalone chats
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow)
    memory_enabled = Column(Boolean, default=True)
    
    # Relationships
    reading = relationship("Reading", back_populates="conversations")
    messages = relationship("ConversationMessage", back_populates="conversation", cascade="all, delete-orphan")


class ConversationMessage(Base):
    """Individual message within a conversation."""
    
    __tablename__ = 'conversation_messages'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey('conversations.id'), nullable=False)
    role = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, nullable=True)  # Additional context or AI metadata
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")


class Memory(Base):
    """AI memory storage for conversations."""
    
    __tablename__ = 'memories'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey('conversations.id'), nullable=False)
    key = Column(String, nullable=False)  # Memory key (e.g., 'user_name', 'important_date')
    value = Column(Text, nullable=False)  # Memory value
    importance_score = Column(Float, default=0.5)  # 0-1 importance for pruning
    created_at = Column(DateTime, default=datetime.utcnow)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation")


class InfluencedReading(Base):
    """Stored AI-generated influenced reading results."""
    
    __tablename__ = 'influenced_readings'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    reading_id = Column(String, ForeignKey('readings.id'), nullable=False)
    ai_summary = Column(Text, nullable=False)
    influenced_cards = Column(JSON, nullable=False)  # Full influenced card data
    advice = Column(JSON, nullable=True)  # List of advice items
    follow_up_questions = Column(JSON, nullable=True)  # List of follow-up questions
    generated_at = Column(DateTime, default=datetime.utcnow)
    model_used = Column(String, nullable=True)  # Which Ollama model was used
    
    # Relationships
    reading = relationship("Reading")


class UserSettings(Base):
    """User preferences and settings."""
    
    __tablename__ = 'user_settings'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    key = Column(String, nullable=False, unique=True)
    value = Column(JSON, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)