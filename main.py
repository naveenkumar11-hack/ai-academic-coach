import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI(title="AI Academic & Career Coach Backend")

# Streamlit frontend connect aaga CORS Middleware
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

# Gemini 2.5 Flash Model Integration Function
def get_gemini_response(prompt: str) -> str:
    current_key = os.getenv("GEMINI_API_KEY")
    if not current_key:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY environment variable is not configured."
        )
    try:
        genai.configure(api_key=current_key)
        # Unga account-il active-aaga irukkum Gemini 2.5 Flash model:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"status": "AI Academic Coach Backend is active and running!"}

# Semester Exam Prep Endpoints (All route aliases included to prevent 404)
@app.post("/api/exam/generate-answer")
@app.post("/api/exam-prep")
@app.post("/generate-exam-answer")
@app.post("/generate-answer")
@app.post("/generate")
@app.post("/ask")
def handle_exam_prep(req: ExamRequest):
    topic = req.topic or req.prompt or "Core Concepts"
    marks = req.mark_format or "12-mark"
    subject = req.subject or "Computer Science & Engineering"

    prompt = f"""
    You are an expert Anna University Professor and Academic Examiner for the CSE (AI & ML) Department.
    Subject: {subject}
    Topic / Question: {topic}
    Mark Format: {marks}

    Generate a complete, high-scoring university exam answer strictly adhering to the {marks} format:

    - If 1-mark:
      Provide a precise 1-2 sentence technical definition, formula, or time complexity.

    - If 2-mark:
      Provide the formal definition, key points/properties, and a 2-line clean example/syntax.

    - If 12-mark:
      1. Title & Anna University Syllabus Mapping
      2. Comprehensive Technical Definition & Significance
      3. Architecture / Working Principle (Include a clean text/ASCII diagram)
      4. Step-by-Step Algorithm / Execution Flow
      5. Clean, Well-Commented Code Implementation (C++ / Python / Java)
      6. Time and Space Complexity Analysis (Best, Worst, and Average cases)
      7. Practical Advantages, Disadvantages & Real-world Applications
      8. Anna University Evaluation Tips (Key keywords examiners look for to award full 12 marks)
    """
    answer = get_gemini_response(prompt)
    return {
        "answer": answer,
        "response": answer,
        "result": answer
    }

# GenAI Mock Interview Endpoint
@app.post("/api/interview")
def handle_interview(req: InterviewRequest):
    if not req.user_answer:
        prompt = f"""
        Act as a Principal AI/GenAI Technical Interviewer.
        Generate 1 practical technical coding/system design question and 1 scenario question for: {req.role}.
        Focus on real-world industry AI problems (LLMs, Transformers, Python, Vector DBs).
        """
    else:
        prompt = f"""
        Role: {req.role}
        Interview Question: {req.question}
        Candidate's Answer: {req.user_answer}

        Evaluate this answer thoroughly as a senior tech interviewer:
        1. Score out of 10
        2. Technical Strengths
        3. Missing Key Concepts & Areas to Improve
        4. Model Answer (Industry Standard)
        """
    result = get_gemini_response(prompt)
    return {
        "feedback": result,
        "response": result,
        "answer": result
    }