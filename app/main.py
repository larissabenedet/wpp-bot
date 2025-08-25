"""
Main FastAPI application entry point.
This is where we configure our API server and include all routes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import webhooks, users
from app.core.config import settings
from app.database.database import engine
from app.database.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI instance
app = FastAPI(
    title="Interview Bot API",
    description="WhatsApp bot for technical interview practice",
    version="1.0.0"
)

# Add CORS middleware for frontend integration later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(webhooks.router, prefix="/webhook", tags=["WhatsApp"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Interview Bot API is running!", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",  # We'll implement this check later
        "whatsapp_api": "configured"
    }