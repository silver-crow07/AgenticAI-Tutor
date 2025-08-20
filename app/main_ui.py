import streamlit as st
from gtts import gTTS
import tempfile
import dashboard
from app.tracker import track_progress, compute_overall
from app.content_engine import get_topic_content
from app.quiz_generator import generate_quiz, parse_quiz
from app.translator import translate_content
from app.tracker import track_progress
from api_utils import clean_text_for_speech, get_explanation

# Initialize session state
if "quiz" not in st.session_state:
    st.session_state.quiz = []
if "show_quiz" not in st.session_state:
    st.session_state.show_quiz = False
if "answers" not in st.session_state:
    st.session_state.answers = []

st.title("📘 Agentic AI Tutor for Class 1–10")

# Inputs
name = st.text_input("Enter your name")
grade = st.selectbox("Select Grade", list(range(1, 11)))
subject = st.selectbox("Subject", ["Math", "Science", "English", "EVS"])
languages = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Tamil": "ta",
    "Bengali": "bn",
    "Telugu": "te",
    "Kannada": "kn",
}
language = st.selectbox("Preferred Language", list(languages.keys()))
selected_lang_code = languages[language]
topic = st.text_input("Enter the topic you want to learn")
level = st.selectbox("Difficulty Level", ["easy", "medium", "hard"])
num_questions = st.slider("Number of Quiz Questions", 1, 10, 5)

# Teach Me Button
if st.button("Teach Me!"):
    content = get_topic_content(subject, topic, grade)
    translated = translate_content(content, language)
    st.subheader("📖 Topic Explanation:")
    st.write(translated)

    explanation = get_explanation(f"Explain {topic} in {level} way")
    st.subheader("📘 AI Explanation:")
    st.markdown(explanation)

    # 🔊 Convert explanation to speech
    cleaned_text = clean_text_for_speech(explanation)
    tts = gTTS(text=cleaned_text, lang=selected_lang_code)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        tts.save(tmpfile.name)
        st.audio(tmpfile.name, format='audio/mp3')

    quiz_text = generate_quiz(topic, level, num_questions)
    if isinstance(quiz_text, str) and "Error" in quiz_text:
        st.error(quiz_text)
    else:
        st.session_state.quiz = parse_quiz(quiz_text)
        st.session_state.show_quiz = True
        st.session_state.answers = [""] * len(st.session_state.quiz)  # initialize answers

# Show Quiz
if st.session_state.show_quiz and st.session_state.quiz:
    st.subheader("📝 Quiz Time:")
    for idx, q in enumerate(st.session_state.quiz):
        user_answer = st.radio(
            f"**Q{idx+1}. {q['question']}**",
            q["options"],
            key=f"user_answer_{idx}"
        )
        # Save index instead of string
        st.session_state.quiz[idx]["user_choice_index"] = q["options"].index(user_answer)

# Submit Answer
if st.button("Submit Answers"):
    score = 0
    debug_info = []

    for idx, q in enumerate(st.session_state.quiz):
        user_idx = q.get("user_choice_index", None)
        correct_idx = q.get("correct_index", None)

        if user_idx == correct_idx:
            score += 1

        user_disp = q["options"][user_idx] if user_idx is not None else "(Not attempted)"
        correct_disp = q["options"][correct_idx] if correct_idx is not None else "(Unknown)"
        debug_info.append(f"Q{idx+1}: User - {user_disp} | Correct - {correct_disp}")

    st.markdown("### 📊 Debug Info (for Dev):")
    for line in debug_info:
        st.markdown(line)

    st.success(f"✅ Your Score: {score}/{len(st.session_state.quiz)}")

    saved = track_progress(name, grade, subject, topic, st.session_state.quiz, score)
    st.info(f"Saved: {saved['correct']}/{saved['total']} ({saved['percent']}%)")

    overall = compute_overall()
    st.subheader("📊 Overall Performance")
    for row in overall:
        st.write(f"{row['name']}: {row['percent']}%  ({row['correct']}/{row['total']})")







