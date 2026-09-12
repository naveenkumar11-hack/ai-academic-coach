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
        "response": output_text,import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

# Gemini API Configuration
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

app = FastAPI(title="AI Academic & Career Coach Backend")

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class ExamRequest(BaseModel):
    subject: Optional[str] = "Data Structures"
    mark_format: Optional[str] = "12-mark"
    topic: Optional[str] = "singly linked list"
    prompt: Optional[str] = None

class InterviewRequest(BaseModel):
    role: Optional[str] = "AI Engineer"
    user_answer: Optional[str] = ""
    question: Optional[str] = ""

def get_gemini_response(prompt: str) -> str:
    current_key = os.getenv("GEMINI_API_KEY")
    if not current_key:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY environment variable is not configured."
        )
    try:
        genai.configure(api_key=current_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"status": "AI Academic Coach Backend is active"}

# Exam Prep Endpoints (Multiple routes supported to avoid 404)
@app.post("/api/exam-prep")
@app.post("/generate-exam-answer")
@app.post("/generate-answer")
@app.post("/generate")
def handle_exam_prep(req: ExamRequest):
    topic = req.topic or req.prompt or "Core Concepts"
    marks = req.mark_format or "12-mark"
    subject = req.subject or "Engineering"

    prompt = f"""
    You are an expert Anna University Professor and Academic Coach for {subject}.
    Provide a comprehensive, high-scoring university exam answer strictly adhering to the {marks} format.

    Topic: {topic}

    Structure guidelines for {marks}:
    - 1-mark: Concise 1-2 sentence precise technical definition or formula.
    - 2-mark: Definition, Key Principle/Property, and a short 2-line syntax/example.
    - 12-mark:
        1. Clear Definition & Need/Significance
        2. Architectural / Working Principle (Include text/ASCII diagram)
        3. Core Algorithm / Code Implementation (Clean C++ or Python syntax)
        4. Time and Space Complexity Analysis
        5. Advantages, Disadvantages & Real-world Applications
        6. Key University Exam Evaluation Tips
    """
    answer = get_gemini_response(prompt)
    return {"answer": answer, "response": answer, "result": answer}

# Mock Interview Endpoint
@app.post("/api/interview")
def handle_interview(req: InterviewRequest):
    if not req.user_answer:
        prompt = f"Generate 1 technical interview question and 1 behavioral scenario question for an entry-level {req.role}."
    else:
        prompt = f"""
        Role: {req.role}
        Interview Question: {req.question}
        Candidate Answer: {req.user_answer}

        Evaluate this answer thoroughly. Provide:
        1. Score out of 10
        2. Strengths
        3. Areas of Improvement
        4. Ideal Industry-standard Answer
        """
    result = get_gemini_response(prompt)
    return {"feedback": result, "response": result, "answer": result}
        "result": output_text
    }

# Alias Endpoint (/ask endru app.py-il irundhaalum idhu work aagum)
@app.post("/ask")
def ask_answer(req: StudyRequest):
    return generate_answer(req)