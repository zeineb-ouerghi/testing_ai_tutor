from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/modules", tags=["modules"])

class Module(BaseModel):
    id: str
    title: str
    description: str

MODULES = [
    {"id": "assessment", "title": "Assessment", "description": "Gauge your current knowledge level."},
    {"id": "fundamentals", "title": "Prompting Fundamentals", "description": "Learn the basics of interacting with AI."},
    {"id": "advanced", "title": "Advanced Prompting", "description": "Master complex prompting techniques."},
    {"id": "practice", "title": "Practice Prompting", "description": "Hands-on exercises to refine your skills."},
    {"id": "genai_fundamentals", "title": "Generative AI Fundamentals", "description": "Understand the core concepts of GenAI."},
]

@router.get("/", response_model=List[Module])
def get_modules():
    return MODULES
