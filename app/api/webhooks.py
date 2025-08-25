"""
WhatsApp webhook endpoints.
This handles incoming messages from WhatsApp Cloud API.
"""
from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import PlainTextResponse
from app.core.config import settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/whatsapp")
async def verify_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_challenge: str = Query(alias="hub.challenge"), 
    hub_verify_token: str = Query(alias="hub.verify_token")
):
    """
    Webhook verification endpoint for WhatsApp Cloud API.
    Meta calls this to verify our webhook URL.
    """
    logger.info(f"Webhook verification attempt with token: {hub_verify_token}")
    
    if hub_mode == "subscribe" and hub_verify_token == settings.webhook_verify_token:
        logger.info("Webhook verified successfully")
        return PlainTextResponse(hub_challenge)
    
    logger.warning("Webhook verification failed")
    raise HTTPException(status_code=403, detail="Verification failed")

@router.post("/whatsapp")
async def receive_message(request: Request):
    """
    Receive incoming WhatsApp messages.
    This is where we'll process user responses and handle commands like STOP.
    """
    try:
        body = await request.json()
        logger.info(f"Received webhook: {body}")
        
        # TODO: Process incoming messages
        # - Extract user phone number and message content
        # - Handle STOP command for unsubscription
        # - Process user responses to questions
        # - Send to AI for analysis
        
        return {"status": "received"}
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")