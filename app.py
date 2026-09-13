import streamlit as st
import requests

st.set_page_config(
    page_title="AI Academic & GenAI Career Coach",
    page_icon="🎓",
    layout="wide"
)

# Local FastAPI Backend URL
BACKEND_URL = "http://127.0.0.1:8000"

st.title("🎓 AI Academic & GenAI Career Coach")
st.caption("Anna University 3rd Sem CSE (AI & ML) Prep & AI Engineering Mock Interview")

tab1, tab2 = st.tabs(["📚 Semester Exam Prep", "💼 GenAI Mock Interview (Text & Voice)"])

# ----------------- Tab 1: Semester Exam Prep -----------------
with tab1:
    st.subheader("Prepare 1-Mark, 2-Mark & 12-Mark Answers")

    col1, col2 = st.columns([2, 1])

    with col1:
        subject = st.selectbox(
            "Select Subject:",
            [
                "CS25C08 - Data Structures",
                "CS25C09 - Object Oriented Programming",
                "MA25C01 - Discrete Mathematics",
                "CS25C10 - Digital Principles and System Design",
                "AI25C01 - Foundations of Machine Learning"
            ]
        )

    with col2:
        mark_format = st.radio(
            "Mark Format:",
            ["1-mark", "2-mark", "12-mark"],
            index=2,
            horizontal=True
        )

    topic = st.text_input(
        "Enter Topic Name:",
        value="Collision Resolution using Quadratic Probing and Double Hashing"
    )

    if st.button("Generate Exam Answer", type="primary"):
        if not topic.strip():
            st.warning("Please enter a topic name.")
        else:
            with st.spinner("Generating Anna University format answer..."):
                payload = {
                    "subject": subject,
                    "mark_format": mark_format,
                    "topic": topic
                }
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/api/exam/generate-answer",
                        json=payload,
                        timeout=90
                    )
                    if response.status_code == 200:
                        data = response.json()
                        result_text = data.get("answer") or data.get("response") or data.get("result")
                        st.success("Answer Generated Successfully!")
                        st.markdown(result_text)
                    else:
                        st.error(f"Backend Error: {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error(
                        "Failed to connect to backend! Make sure FastAPI uvicorn backend is running in the terminal."
                    )
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ------------- Tab 2: GenAI Mock Interview -------------
with tab2:
    st.subheader("AI Engineering Mock Interview")
    role = st.selectbox(
        "Target Role:",
        ["GenAI Engineer", "Machine Learning Engineer", "Full Stack AI Developer"]
    )

    if st.button("Get Interview Question"):
        with st.spinner("Fetching questions..."):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/api/interview",
                    json={"role": role},
                    timeout=60
                )
                if res.status_code == 200:
                    st.session_state["current_question"] = res.json().get("feedback", "")
                else:
                    st.error(f"Error: {res.text}")
            except Exception as e:
                st.error(f"Backend error: {str(e)}")

    if "current_question" in st.session_state:
        st.info(st.session_state["current_question"])
        user_reply = st.text_area("Type your technical response here:", height=150)

        if st.button("Submit Answer for Evaluation"):
            if not user_reply.strip():
                st.warning("Please type your response before submitting.")
            else:
                with st.spinner("Evaluating response with AI panel..."):
                    try:
                        res = requests.post(
                            f"{BACKEND_URL}/api/interview",
                            json={
                                "role": role,
                                "question": st.session_state["current_question"],
                                "user_answer": user_reply
                            },
                            timeout=90
                        )
                        if res.status_code == 200:
                            st.markdown(res.json().get("feedback", ""))
                        else:
                            st.error(f"Error: {res.text}")
                    except Exception as e:
                        st.error(f"Backend error: {str(e)}")