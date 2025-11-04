import os
import json
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import openai
from dotenv import load_dotenv

from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

# Load environment variables from .env file
load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- OpenAI Client Setup ---
# It's recommended to set the OPENAI_API_KEY environment variable
# You can do this in a .env file at the root of the backend directory
# OPENAI_API_KEY="your-api-key-here"
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- CORS Middleware ---
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- System Prompt for the AI ---
SYSTEM_PROMPT = """
You are an expert product manager. Your task is to analyze unstructured text from various sources (like customer feedback, meeting notes, or feature ideas) and convert it into a structured task.

The user will provide a piece of text. You must extract the core request and format it as a JSON object with the following fields:
- "description": A concise summary of the task or issue.
- "type": Classify the task as one of three types: 'feature', 'pain_point', or 'enhancement'.
- "priority": Assign a priority level: 'High', 'Medium', or 'Low'. Base this on implied urgency, impact, or keywords.
- "user_story": Generate a clear user story in the format "As a [user type], I want to [action] so that [benefit]."
- "acceptance_criteria": Write a simple set of acceptance criteria in the format "Given [context], when [action], then [outcome]."

Your response must be only the JSON object, with no other text or explanations.
"""


@app.get("/")
def read_root():
    return {"message": "Welcome to the Product Management API"}

@app.get("/api/tasks", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks

@app.get("/api/roadmap")
def get_roadmap_data(db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, limit=1000) # Get all tasks for the roadmap

    # Group tasks by priority
    roadmap_data = {
        "High": [],
        "Medium": [],
        "Low": [],
    }
    for task in tasks:
        if task.priority in roadmap_data:
            roadmap_data[task.priority].append(schemas.Task.from_orm(task).dict())

    return roadmap_data

@app.post("/api/process", response_model=schemas.Task)
async def process_text(request: schemas.TextInput, db: Session = Depends(get_db)):
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key is not configured. Please set the OPENAI_API_KEY environment variable.")

    try:
        response = await openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.text},
            ],
            response_format={"type": "json_object"},
        )

        ai_response_text = response.choices[0].message.content
        task_data = json.loads(ai_response_text)

        # Validate the structure of the AI's response
        task_to_create = schemas.TaskCreate(**task_data)

        return crud.create_task(db=db, task=task_to_create)

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse the response from the AI.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing with OpenAI: {str(e)}")
