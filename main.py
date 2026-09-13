import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI(title="AI Academic & GenAI Career Coach Backend")

# Streamlit frontend connect seivadharku CORS Middleware
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
    role: Optional[str] = "GenAI Engineer"
    user_answer: Optional[str] = ""
    question: Optional[str] = ""

def get_gemini_response(prompt: str) -> str:
    current_key = os.getenv("GEMINI_API_KEY")
    if not current_key:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY environment variable is missing. Set it in the terminal."
        )
    
    genai.configure(api_key=current_key)

    # Models fallback list (model version issue thavirkka)
    candidate_models = ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-pro"]
    last_error = None

    for model_name in candidate_models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text
        except Exception as e:
            last_error = e
            continue

    raise HTTPException(
        status_code=500,
        detail=f"Gemini API Error: {str(last_error)}. Please verify your Google AI Studio API key."
    )

@app.get("/")
def home():
    return {"status": "AI Academic Coach Backend is active and running!"}

# Primary Exam Preparation Endpoints (Matches your frontend request URL)
@app.post("/api/exam/generate-answer")
@app.post("/api/exam-prep")
@app.post("/generate-exam-answer")
@app.post("/generate")
@app.post("/ask")
def handle_exam_prep(req: ExamRequest):
    topic = req.topic or req.prompt or "Core Concepts"
    marks = req.mark_format or "12-mark"
    subject = req.subject or "Computer Science and Engineering"

    prompt = f"""
    You are an expert Anna University Professor and Academic Examiner for the CSE (AI & ML) Department.
    Subject: {subject}
    Question/Topic: {topic}
    Mark Format: {marks}

    Generate a complete, high-scoring university exam answer strictly following this structure:

    IF 1-MARK:
    - Precise 1-2 sentence technical definition, formula, or time complexity.

    IF 2-MARK:
    - Formal Definition
    - Key Characteristics / Rules (2-3 bullet points)
    - Short Syntax, Expression, or Example

    IF 12-MARK:
    1. Title & Anna University Syllabus Mapping
    2. Comprehensive Technical Definition & Significance
    3. Architecture / Working Principle (Include a clean text/ASCII diagram)
    4. Step-by-Step Algorithm / Execution Flow
    5. Clean, Well-Commented Code Implementation (C++ / Python / Java)
    6. Time and Space Complexity Analysis (Best, Worst, Average cases)
    7. Practical Advantages, Disadvantages & Real-world Applications
    8. Anna University Key Answer Scoring Tips (What examiners look for to award full 12 marks)
    """
    answer = get_gemini_response(prompt)
    return {
        "answer": answer,
        "response": answer,
        "result": answer
    }

# Mock Interview Endpoint
@app.post("/api/interview")
def handle_interview(req: InterviewRequest):
    if not req.user_answer:
        prompt = f"""
        Act as a Principal AI/GenAI Technical Interviewer at a top tier company.
        Generate 1 practical technical question and 1 scenario question for a candidate applying for: {req.role}.
        Keep it challenging and relevant to modern LLMs, Transformers, Python, and ML systems.
        """
    else:
        prompt = f"""
        Role: {req.role}
        Interview Question: {req.question}
        Candidate's Answer: {req.user_answer}

        Evaluate this answer objectively as a senior tech interviewer:
        1. Rating: [Score / 10]
        2. Technical Strengths
        3. Missing Concepts or Areas to Improve
        4. Model Answer (Industry Standard)
        """
    result = get_gemini_response(prompt)
    return {
        "feedback": result,
        "response": result,
        "answer": result
    }