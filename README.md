# AI Tutor Agent

A multi-agent tutoring system with backend powered by Google Gemini (via Google ADK) and a modern web frontend.

## Features

- **Multi-agent system**: Handles math & physics queries via specialized sub-agents
- **Tool-enhanced**: Uses computational tools for accurate answers
- **Web UI**: Clean chat interface similar to DeepSeek
- **REST API**: FastAPI backend with `/ask` endpoint

## Tech Stack

**Backend**  
FastAPI · Google ADK · Gemini API · Railway

**Frontend**  
HTML5 · CSS3 · JavaScript · Vercel

## Quick Start

### Backend Setup
```bash
git clone https://github.com/Akshaj77/AI-Tutor-final.git
cd AI-Tutor-final/backend

# 1. Set up environment
echo "GOOGLE_API_KEY=your_key_here" > .env

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run locally
uvicorn main:app --reload

```
## Frontend
cd ../frontend

# 1. Configure API endpoint (edit index.html)
const API_ENDPOINT = "https://your-railway-app.up.railway.app/ask";

# 2. Deploy to Vercel
vercel deploy

##Project Structure 
AI-Tutor-final/
├── backend/
│   ├── main.py               # FastAPI app
│   ├── agent/                # ADK agent implementation
│   └── requirements.txt
├── frontend/
│   ├── index.html            # Chat UI
│   ├── styles.css            # Responsive design
│   └── script.js             # API interaction
└── README.md

## API Documentation
Interactive docs available at:

Local: http://localhost:8080/docs

Production: https://your-railway-app.up.railway.app/docs

#Deployment Guides
##Backend(Railway)

Connect GitHub repo

Set GOOGLE_API_KEY in environment variables

Deploy!

## Frontend(Vercel)
Import frontend folder

Set build command: None (static site)

Deploy!
Check final tool here : https://ai-tutor-frontend-gules.vercel.app/

## Screenshots 
<img width="866" alt="image" src="https://github.com/user-attachments/assets/1e685da0-c403-408c-a0e1-cc95de504592" />
