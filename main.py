import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

# Gemini API Configuration
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

app = FastAPI(title="AI Academic Coach API")

# CORS Middleware (Streamlit frontend connect seivadharku)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Flexible Request Schema (prompt, question, or topic - edhai anuppinaalum eduthukkollum)
class StudyRequest(BaseModel):
    prompt: Optional[str] = None
    question: Optional[str] = None
    topic: Optional[str] = None
    marks: Optional[str] = "16"
    subject: Optional[str] = "Computer Science / Engineering"

def generate_academic_response(user_query: str, marks: str, subject: str) -> str:
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY environment variable not set."
        )

    # Academic Exam Coach System Prompt
    system_prompt = f"""
    You are an expert University Professor and AI Academic Coach for {subject}.
    Provide a comprehensive, high-scoring university exam-oriented answer for the following question/topic for a {marks}-mark question.

    Structure the response clearly using Markdown:
    1. Definition & Core Concept
    2. Detailed Explanation & Architecture/Working Principle
    3. Key Components / Characteristics / Types
    4. Code Snippet, Example, or Diagrammatic Representation (ASCII/text-based)
    5. Advantages & Disadvantages / Applications
    6. University Exam Tips / Key Takeaways

    Topic/Question: {user_query}
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(system_prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"status": "AI Academic Coach Backend is running successfully!"}

# Primary Endpoint
@app.post("/generate")
def generate_answer(req: StudyRequest):
    query = req.prompt or req.question or req.topic
    if not query:
        raise HTTPException(status_code=400, detail="Please provide a prompt, question, or topic.")
    
    output_text = generate_academic_response(query, req.marks, req.subject)
    
    # Frontend edhaavathu key thedinaalum support seiyum response format
    return {
        "answer": output_text,
        "response": output_text,
        "result": output_text
    }

# Alias Endpoint (/ask endru app.py-il irundhaalum idhu work aagum)
@app.post("/ask")
def ask_answer(req: StudyRequest):
    return generate_answer(req)