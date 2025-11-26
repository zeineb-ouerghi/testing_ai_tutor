from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from ..database import get_db
from ..models import ChatSession, Message, User
import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession as VertexChatSession
from fastapi.responses import StreamingResponse
import os
import asyncio

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    user_id: int
    module_id: str
    message: str
    session_id: Optional[int] = None

class MessageResponse(BaseModel):
    role: str
    content: str

# System Prompts Configuration
SYSTEM_PROMPTS = {
    "assessment": "You are an AI Tutor conducting an assessment. Ask the user questions to gauge their understanding of AI and Prompt Engineering. Ask one question at a time. Be encouraging but objective.",
    "fundamentals": "You are an AI Tutor teaching Prompting Fundamentals. Explain concepts clearly, use examples, and ensure the user understands before moving on. Topics: Zero-shot, Few-shot, Chain of thought.",
    "advanced": "You are an expert AI Tutor teaching Advanced Prompting. Cover topics like ReAct, Self-Consistency, and Prompt Chaining. Assume the user has basic knowledge.",
    "practice": "You are a Practice Partner. Give the user coding or writing challenges and provide feedback on their prompts. Don't just give the answer, guide them.",
    "genai_fundamentals": "You are an AI Tutor teaching Generative AI Fundamentals. Explain how LLMs work, tokens, context windows, and temperature. Keep it accessible.",
}

@router.post("/message")
async def send_message(request: ChatRequest, db: Session = Depends(get_db)):
    # 1. Get or Create Session
    if request.session_id:
        session = db.query(ChatSession).filter(ChatSession.id == request.session_id).first()
        if not session:
             raise HTTPException(status_code=404, detail="Session not found")
    else:
        session = ChatSession(user_id=request.user_id, module_id=request.module_id)
        db.add(session)
        db.commit()
        db.refresh(session)

    # 2. Save User Message
    user_msg = Message(session_id=session.id, role="user", content=request.message)
    db.add(user_msg)
    db.commit()

    # 3. Prepare Vertex AI Chat
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    if not project_id:
        # Fallback for demo if no project provided
        print("Warning: GOOGLE_CLOUD_PROJECT not set.")
        # We might want to raise error or handle gracefully
    
    try:
        vertexai.init(project=project_id, location=location)
        model = GenerativeModel("gemini-1.5-flash")
        
        # Construct history for Vertex AI
        # Vertex AI expects history as a list of Content objects or similar structure
        # For simplicity, we can use the chat session object if we maintain it, 
        # but since we are stateless between requests here, we reconstruct history.
        
        history_msgs = db.query(Message).filter(Message.session_id == session.id).order_by(Message.timestamp).all()
        
        # We need to format history for Vertex AI
        # Vertex AI history format: [Content(role="user", parts=[...]), Content(role="model", parts=[...])]
        # Note: The current message is NOT in history for start_chat, we send it in send_message
        
        chat_history = []
        system_prompt = SYSTEM_PROMPTS.get(request.module_id, "You are a helpful AI Tutor.")
        
        # Vertex AI supports system instructions in the model init, but let's just prepend if needed or use system_instruction arg
        model = GenerativeModel("gemini-1.5-flash", system_instruction=[system_prompt])
        
        # Filter out the current message we just saved from history to avoid duplication if we were to use it in start_chat
        # Actually, we just saved it. So it IS in history_msgs.
        # We should exclude the very last message (which is the current one) from history passed to start_chat
        # and send it as the message.
        
        # Let's separate previous history and current message
        previous_msgs = history_msgs[:-1] # All except last
        current_msg_content = history_msgs[-1].content # The last one
        
        from vertexai.generative_models import Content, Part
        
        for msg in previous_msgs:
            role = "user" if msg.role == "user" else "model"
            chat_history.append(Content(role=role, parts=[Part.from_text(msg.content)]))

        chat = model.start_chat(history=chat_history)
        
        async def generate():
            full_response = ""
            # stream=True returns an iterable
            responses = await chat.send_message_async(current_msg_content, stream=True)
            async for chunk in responses:
                content = chunk.text
                full_response += content
                yield content
            
            # Save AI Message after streaming
            # Workaround: Create a new session manually to save.
            from ..database import SessionLocal
            db_new = SessionLocal()
            ai_msg = Message(session_id=session.id, role="ai", content=full_response)
            db_new.add(ai_msg)
            db_new.commit()
            db_new.close()

        return StreamingResponse(generate(), media_type="text/plain")

    except Exception as e:
        print(f"Error calling Vertex AI: {e}")
        # Fallback
        async def mock_generate():
            response = f"Echo (Vertex AI Error): {request.message}. Error: {str(e)}"
            yield response
            
            from ..database import SessionLocal
            db_new = SessionLocal()
            ai_msg = Message(session_id=session.id, role="ai", content=response)
            db_new.add(ai_msg)
            db_new.commit()
            db_new.close()
            
        return StreamingResponse(mock_generate(), media_type="text/plain")

@router.get("/history/{session_id}")
def get_history(session_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.timestamp).all()
    return messages
