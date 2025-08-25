"""
CRUD operations for database models.
These functions handle creating, reading, updating, and deleting data.
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.database.models import User, Question, UserResponse, TechArea, Language
from typing import Optional, List
from datetime import datetime

# User CRUD operations
def create_user(db: Session, whatsapp_number: str, name: Optional[str], 
                preferred_language: Language, tech_area: TechArea) -> User:
    """Create a new user"""
    db_user = User(
        whatsapp_number=whatsapp_number,
        name=name,
        preferred_language=preferred_language,
        tech_area=tech_area
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_whatsapp(db: Session, whatsapp_number: str) -> Optional[User]:
    """Get user by WhatsApp number"""
    return db.query(User).filter(User.whatsapp_number == whatsapp_number).first()

def get_active_users(db: Session) -> List[User]:
    """Get all active users"""
    return db.query(User).filter(User.is_active == True).all()

def deactivate_user(db: Session, whatsapp_number: str) -> bool:
    """Deactivate user (for STOP command)"""
    user = get_user_by_whatsapp(db, whatsapp_number)
    if user:
        user.is_active = False
        db.commit()
        return True
    return False

def update_last_question_sent(db: Session, user_id: int):
    """Update when last question was sent to user"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.last_question_sent = datetime.utcnow()
        db.commit()

# Question CRUD operations
def create_question(db: Session, tech_area: TechArea, difficulty: str,
                   question_text_en: str, question_text_es: Optional[str] = None,
                   question_text_pt: Optional[str] = None,
                   expected_concepts: Optional[str] = None) -> Question:
    """Create a new question"""
    db_question = Question(
        tech_area=tech_area,
        difficulty=difficulty,
        question_text_en=question_text_en,
        question_text_es=question_text_es,
        question_text_pt=question_text_pt,
        expected_concepts=expected_concepts
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def get_questions_by_area(db: Session, tech_area: TechArea) -> List[Question]:
    """Get all questions for a specific tech area"""
    return db.query(Question).filter(Question.tech_area == tech_area).all()

def get_random_question(db: Session, tech_area: TechArea, 
                       exclude_answered_by_user: Optional[int] = None) -> Optional[Question]:
    """Get a random question that user hasn't answered recently"""
    query = db.query(Question).filter(Question.tech_area == tech_area)
    
    if exclude_answered_by_user:
        # Exclude questions answered by this user in last 30 days
        # This is a simplified version - you might want more complex logic
        answered_question_ids = db.query(UserResponse.question_id).filter(
            and_(
                UserResponse.user_id == exclude_answered_by_user,
                UserResponse.created_at >= datetime.utcnow().replace(day=1)  # This month
            )
        ).subquery()
        
        query = query.filter(~Question.id.in_(answered_question_ids))
    
    return query.order_by(func.random()).first()

# Response CRUD operations
def create_user_response(db: Session, user_id: int, question_id: int,
                        response_text: str, response_type: str = "text") -> UserResponse:
    """Create a new user response"""
    db_response = UserResponse(
        user_id=user_id,
        question_id=question_id,
        response_text=response_text,
        response_type=response_type
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response

def update_response_feedback(db: Session, response_id: int, 
                           ai_feedback: str, score: int):
    """Update response with AI feedback and score"""
    response = db.query(UserResponse).filter(UserResponse.id == response_id).first()
    if response:
        response.ai_feedback = ai_feedback
        response.score = score
        db.commit()
        return response
    return None

def get_user_responses(db: Session, user_id: int) -> List[UserResponse]:
    """Get all responses from a user"""
    return db.query(UserResponse).filter(UserResponse.user_id == user_id).all()