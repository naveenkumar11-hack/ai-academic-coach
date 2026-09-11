import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# Environment variable-l irunthu API key-a safe-ah edukkurom
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

class RequestModel(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"message": "AI Academic Coach Backend is running!"}

@app.post("/generate")
def generate_response(data: RequestModel):
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not found in environment variables")
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(data.prompt)
        return {"result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))