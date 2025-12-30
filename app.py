import streamlit as st
from PIL import Image

from agents.parser_agent import parse_problem
from agents.router_agent import route_problem
from agents.solver_agent import solve_problem
from agents.verifier_agent import verify_solution
from agents.explainer_agent import explain_solution
from utils.ocr import extract_text_from_image
from utils.voice_utils import listen_voice, speak_text, audio_file_to_text
from utils.feedback_utils import log_feedback

st.set_page_config(page_title="Multimodal Math Mentor", layout="wide")
st.title("🧮 Multimodal Math Mentor")

# ------------------ Initialize session state ------------------
if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""
if "solution" not in st.session_state:
    st.session_state.solution = None
if "parsed" not in st.session_state:
    st.session_state.parsed = None
if "route" not in st.session_state:
    st.session_state.route = None
if "verification" not in st.session_state:
    st.session_state.verification = None
if "explanation" not in st.session_state:
    st.session_state.explanation = []

# ------------------ Input Mode ------------------
mode = st.selectbox("Choose input mode", ["Text", "Image", "Voice"])
question = ""

# ------------------ Text Input ------------------
if mode == "Text":
    question = st.text_area("Enter a math problem")

# ------------------ Image Input ------------------
elif mode == "Image":
    uploaded = st.file_uploader("Upload an image of a math problem", type=["png", "jpg", "jpeg"])
    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        extracted_text, confidence = extract_text_from_image(image)
        st.subheader("🔍 OCR Extracted Text (Editable)")
        question = st.text_area("Edit the extracted text if needed", extracted_text)
        st.progress(int(confidence * 100))
        if confidence < 0.5:
            st.warning("⚠️ OCR confidence is low. Please verify the text.")

# ------------------ Voice Input ------------------
elif mode == "Voice":
    st.write("🎤 Upload an audio file of the problem")
    uploaded_audio = st.file_uploader("Upload audio (.wav/.mp3)", type=["wav", "mp3"])
    if uploaded_audio:
        temp_file_path = "temp_audio_file.wav"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_audio.read())

        voice_text = audio_file_to_text(temp_file_path)
        if voice_text:
            st.session_state.voice_text = voice_text
            st.success(f"Transcribed from audio: {voice_text}")
        else:
            st.error("Could not recognize audio. Try again.")

    question = st.session_state.voice_text
    if question:
        question = st.text_area("Edit the recognized text if needed", value=question)

# ------------------ Solve Pipeline ------------------
if st.button("Solve", key="solve_btn"):
    if question.strip() == "":
        st.warning("Please provide a math problem.")
    else:
        # 1️⃣ Parse
        parsed = parse_problem(question)
        st.session_state.parsed = parsed
        st.subheader("Parsed Output")
        st.json(parsed)

        # 2️⃣ Route
        route = route_problem(parsed)
        st.session_state.route = route
        st.subheader("Routing Decision")
        st.json(route)

        # 3️⃣ Solve
        solution = solve_problem(parsed, route)
        st.session_state.solution = solution
        st.subheader("Solver Output")
        st.json(solution)

        # 4️⃣ Verify
        verification = verify_solution(solution)
        st.session_state.verification = verification
        st.subheader("Verification")
        st.json(verification)

        # 5️⃣ Explain
        explanation = []
        if verification.get("valid", False):
            explanation = explain_solution(parsed, solution)
            st.session_state.explanation = explanation
            st.subheader("📘 Explanation")
            for step in explanation:
                st.write("- ", step)

            if st.button("Read Explanation", key="read_expl_btn"):
                speak_text(" ".join(explanation))
        else:
            st.error("Solution could not be verified.")

# ------------------ Feedback Section ------------------
if st.session_state.solution is not None:
    st.subheader("Was this solution correct?")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Correct", key="correct_btn"):
            log_feedback(question, st.session_state.solution, "✅")
            st.success("Thanks for your feedback!")

    with col2:
        incorrect_comment = st.text_input("❌ Incorrect? Provide correct solution or comment:", key="incorrect_input")
        if st.button("Submit Feedback ❌", key="incorrect_btn"):
            if incorrect_comment.strip() == "":
                st.warning("Please provide a comment or correct solution.")
            else:
                log_feedback(question, st.session_state.solution, "❌", incorrect_comment)
                st.success("Thanks! Feedback logged for learning.")
