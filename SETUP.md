# Setup Guide

## Prerequisites
- Python 3.8+ installed
- Meta Business Account (already configured ✅)
- WhatsApp Cloud API access
- Basic understanding of REST APIs

## Development Environment Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file with:
```
WHATSAPP_ACCESS_TOKEN=your_token_here
WHATSAPP_PHONE_NUMBER_ID=your_phone_id_here
WEBHOOK_VERIFY_TOKEN=your_webhook_token_here
DATABASE_URL=sqlite:///./interview_bot.db
OPENAI_API_KEY=your_openai_key_here
```

### 4. Run the Application
```bash
uvicorn app.main:app --reload
```