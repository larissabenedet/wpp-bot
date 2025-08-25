"""
User management endpoints.
This handles user registration from the web form.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class TechArea(str, Enum):
    """Available technical areas for questions"""
    JAVASCRIPT = "javascript"
    PYTHON = "python" 
    RUBY = "ruby"
    GO = "go"
    DSA = "dsa"  # Data Structures & Algorithms

class Language(str, Enum):
    """Available interface languages"""
    ENGLISH = "en"
    SPANISH = "es"
    PORTUGUESE = "pt"

class UserRegistration(BaseModel):
    """User registration data from web form"""
    whatsapp_number: str = Field(..., description="WhatsApp number with country code")
    preferred_language: Language = Field(..., description="Interface language")
    tech_area: TechArea = Field(..., description="Area of technical questions")
    agreed_to_messages: bool = Field(..., description="Consent to receive messages")
    name: str = Field(..., description="User's name")

@router.post("/register")
async def register_user(user_data: UserRegistration):
    """
    Register a new user for the interview bot.
    This endpoint will be called by the frontend form.
    """
    try:
        logger.info(f"New user registration: {user_data.whatsapp_number}")
        
        # Validate consent
        if not user_data.agreed_to_messages:
            raise HTTPException(
                status_code=400, 
                detail="User must agree to receive messages"
            )
        
        # TODO: Save user to database
        # TODO: Send welcome message via WhatsApp
        # TODO: Schedule first question
        
        return {
            "message": "User registered successfully",
            "whatsapp_number": user_data.whatsapp_number,
            "tech_area": user_data.tech_area,
            "language": user_data.preferred_language,
            "name": user_data.name
        }
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@router.post("/unsubscribe/{whatsapp_number}")
async def unsubscribe_user(whatsapp_number: str):
    """
    Unsubscribe user from daily questions.
    This can be called via STOP command or web interface.
    """
    try:
        logger.info(f"Unsubscribing user: {whatsapp_number}")
        
        # TODO: Mark user as inactive in database
        # TODO: Cancel scheduled questions
        
        return {"message": "User unsubscribed successfully"}
        
    except Exception as e:
        logger.error(f"Unsubscribe error: {e}")
        raise HTTPException(status_code=500, detail="Unsubscribe failed")