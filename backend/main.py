import os
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, HTTPException
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from uuid import uuid4
from google.genai import types
from multi_tool_agent.agent import root_agent  
from dotenv import load_dotenv  
import traceback
from fastapi.middleware.cors import CORSMiddleware  

# Load environment variables from .env file
load_dotenv()  # This loads variables from .env into os.environ

if os.getenv("GOOGLE_API_KEY"):
    # Using Google AI Studio
    print(os.getenv("GOOGLE_API_KEY"))
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
else:
    raise RuntimeError("Missing Google AI or Vertex AI credentials in .env")

# Initialize components
session_service = InMemorySessionService()
APP_NAME = "AI_Tutor_App"

# Create FastAPI app


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (replace with your frontend URL in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    prompt: str
    user_id: str = "default_user"
    session_id: str = None

@app.post("/ask")
async def ask_agent(request: AskRequest):
    """Endpoint to interact with the agent"""
    try:
        # Use provided session_id or generate a new one
        session_id = request.session_id or str(uuid4())
        
        # Create or get existing session
        session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=request.user_id,
            session_id=session_id
        )
        
        if not session:
            session = await session_service.create_session(
                app_name=APP_NAME,
                user_id=request.user_id,
                session_id=session_id
            )
            print(f"Created new session: {session_id}")
        else:
            print(f"Using existing session: {session_id}")

        # Initialize runner with your agent
        # (You'll need to import/initialize your agent properly)
        runner = Runner(
            agent=root_agent,  # Make sure root_agent is properly imported/initialized
            app_name=APP_NAME,
            session_service=session_service
        )

        # Prepare message
        content = types.Content(role='user', parts=[types.Part(text=request.prompt)])
        
        # Process the request
        final_response = None
        async for event in runner.run_async(
            user_id=request.user_id,
            session_id=session_id,
            new_message=content
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response = event.content.parts[0].text
                break

        if not final_response:
            final_response = "Agent did not produce a valid response"

        return {
            "response": final_response,
            "session_id": session_id,
            "user_id": request.user_id
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))