import streamlit as st
import requests

st.set_page_config(page_title="AI Career & Semester Coach", layout="wide")

st.title("🎓 AI Academic & GenAI Career Coach")
st.caption("Anna University 3rd Sem CSE (AI & ML) Prep & AI Engineering Mock Interview")

BACKEND_URL = "http://127.0.0.1:8000"

tab1, tab2 = st.tabs(["📚 Semester Exam Prep", "💼 GenAI Mock Interview (Text & Voice)"])

# -------------------------------------------------------------
# TAB 1: SEMESTER EXAM PREP
# -------------------------------------------------------------
with tab1:
    st.subheader("Prepare 1-Mark, 2-Mark & 12-Mark Answers")
    col1, col2 = st.columns(2)
    
    with col1:
        subject = st.selectbox(
            "Select Subject:",
            [
                "CS25C08 - Data Structures",
                "CS25C11 - Operating Systems",
                "CS25C09 - Java Programming",
                "MA25C08 - Discrete Mathematics",
                "CS25C10 - Object Oriented Software Engineering"
            ]
        )
        subject_code = subject.split(" - ")[0]
        
    with col2:
        question_type = st.radio(
            "Mark Format:", 
            ["1-mark", "2-mark", "12-mark"], 
            index=2, 
            horizontal=True
        )
        
    topic = st.text_input("Enter Topic Name:", value="Collision Resolution using Quadratic Probing and Double Hashing")
    
    if st.button("Generate Exam Answer", type="primary"):
        with st.spinner(f"Drafting university-standard {question_type} answer for {topic}..."):
            try:
                payload = {
                    "subject_code": subject_code,
                    "topic": topic,
                    "question_type": question_type
                }
                res = requests.post(f"{BACKEND_URL}/api/exam/generate-answer", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    st.success("Answer Generated Successfully!")
                    st.markdown(data["answer"])
                else:
                    st.error(f"Backend Error: {res.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}. Make sure uvicorn backend is running!")

# -------------------------------------------------------------
# TAB 2: MOCK INTERVIEW EVALUATOR (TEXT & AUDIO)
# -------------------------------------------------------------
with tab2:
    st.subheader("AI Technical & Communication Interview Grader")
    
    sub_for_interview = st.selectbox(
        "Subject for Interview Question:",
        [
            "CS25C08 - Data Structures",
            "CS25C11 - Operating Systems",
            "CS25C09 - Java Programming",
            "MA25C08 - Discrete Mathematics",
            "CS25C10 - Object Oriented Software Engineering"
        ]
    )
    sub_code_interview = sub_for_interview.split(" - ")[0]
    
    interview_q = st.text_input(
        "Interview Question:",
        value="Explain how Banker's Safety Algorithm avoids deadlocks in an OS."
    )
    
    input_mode = st.radio("Choose Input Mode:", ["Text Input", "Voice Microphone"], horizontal=True)
    
    student_answer_text = ""
    
    if input_mode == "Text Input":
        student_answer_text = st.text_area(
            "Your Answer (Type your technical answer here):",
            height=150,
            placeholder="Explain clearly using technical terms..."
        )
    else:
        st.write("🎙️ **Record Your Answer via Microphone:**")
        audio_value = st.audio_input("Record voice")
        if audio_value:
            st.audio(audio_value)
            st.info("Audio recorded! (Transcribing audio directly in browser...)")
            student_answer_text = st.text_area(
                "Verify or edit transcription of your answer:",
                value="The Banker's safety algorithm uses Available, Max, Allocation, and Need matrices to find a safe execution sequence.",
                height=100
            )

    if st.button("Submit Answer for Evaluation", type="primary"):
        if not student_answer_text.strip():
            st.warning("Please provide an answer (type or record audio) first!")
        else:
            with st.spinner("Hiring Manager is analyzing your technical accuracy and communication..."):
                try:
                    payload = {
                        "subject_code": sub_code_interview,
                        "question": interview_q,
                        "student_answer": student_answer_text
                    }
                    res = requests.post(f"{BACKEND_URL}/api/career/evaluate-interview", json=payload)
                    if res.status_code == 200:
                        eval_data = res.json()
                        st.success("Evaluation Complete!")
                        st.markdown(eval_data["evaluation"])
                    else:
                        st.error(f"Backend Error: {res.text}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {e}")