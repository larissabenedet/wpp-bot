"""
Database models for the Interview Bot.
These define the structure of our database tables.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base
import enum

class TechArea(enum.Enum):
    """Technical areas for questions"""
    JAVASCRIPT = "javascript"
    PYTHON = "python"
    RUBY = "ruby"
    DSA = "dsa"

class Language(enum.Enum):
    """Interface languages"""
    ENGLISH = "en"
    SPANISH = "es"
    PORTUGUESE = "pt"

class User(Base):
    """User model - stores registered users"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    whatsapp_number = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    preferred_language = Column(Enum(Language), nullable=False)
    tech_area = Column(Enum(TechArea), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_question_sent = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    responses = relationship("UserResponse", back_populates="user")

class Question(Base):
    """Question model - stores technical interview questions"""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    tech_area = Column(Enum(TechArea), nullable=False)
    difficulty = Column(String, nullable=False)  # "easy", "medium", "hard"
    question_text_en = Column(Text, nullable=False)
    question_text_es = Column(Text, nullable=True)
    question_text_pt = Column(Text, nullable=True)
    expected_concepts = Column(Text, nullable=True)  # JSON string with key concepts
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    responses = relationship("UserResponse", back_populates="question")

class UserResponse(Base):
    """User response model - stores user answers and AI feedback"""
    __tablename__ = "user_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    response_text = Column(Text, nullable=False)
    response_type = Column(String, nullable=False)  # "text" or "audio"
    ai_feedback = Column(Text, nullable=True)
    score = Column(Integer, nullable=True)  # 1-10 score from AI
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="responses")
    question = relationship("Question", back_populates="responses")