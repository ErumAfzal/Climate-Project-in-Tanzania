import streamlit as st
import os
import openai
from PyPDF2 import PdfReader
from docx import Document
from typing import List

# Set OpenAI API key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# ------------------------------------
# File Handling Functions
# ------------------------------------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    elif file.name.endswith(".docx"):
        return extract_text_from_docx(file)
    else:
        return file.read().decode("utf-8")

# ------------------------------------
# OpenAI Question Generation
# ------------------------------------
def generate_questions_with_openai(text, q_type, count):
    system_prompt = (
        "You are an expert educator creating academic-level assessment questions "
        "aligned with EQF Level 6–7 (Bachelor/Master). The questions should reflect deep understanding "
        "of pedagogical theory, including Habermas’ theory of communicative action, role-play evaluation, "
        "strategic vs. understanding-oriented communication, and real-world teacher training."
    )

    user_prompt = (
        f"Based on the following content:\n\n"
        f"{text[:4000]}\n\n"  # limit text for prompt token length
        f"Generate {count} {q_type} questions suitable for Master's-level students in education. "
        f"Each question must be theory-informed, practice-relevant, and unambiguous."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5,
        max_tokens=1500
    )

    output = response.choices[0].message.content
    return output.strip().split("\n\n")

# ------------------------------------
# Streamlit UI
# ------------------------------------
st.set_page_config(page_title="EQF 6–7 Question Generator", layout="wide")
st.title("🎓 EQF 6–7 Pedagogical Question Generator with OpenAI")
st.markdown("Upload documents to generate **master’s-level questions** based on pedagogical theory and real-world teacher education contexts.")

uploaded_files = st.file_uploader("📄 Upload PDF, DOCX, or TXT files", type=["pdf", "docx", "txt"], accept_multiple_files=True)

st.markdown("### 🎯 Select Target Number of Questions")
default_targets = {
    "Multiple Choice / Single or Multi-select": 6,
    "Zuordnung (Matching)": 2,
    "Open Text Questions": 4,
    "Quantitative / Numerical Entry": 2,
    "Scenario / Applied Pedagogy MCQ": 2
}

question_targets = {}
cols = st.columns(len(default_targets))
for i, (qtype, default) in enumerate(default_targets.items()):
    with cols[i]:
        question_targets[qtype] = st.number_input(qtype, min_value=0, value=default, key=qtype)

if st.button("🚀 Generate Questions"):
    if not uploaded_files:
        st.warning("⚠️ Please upload at least one document.")
    else:
        with st.spinner("🧠 Extracting and analyzing text..."):
            all_text = "\n\n".join([extract_text(file) for file in uploaded_files])

        st.success("✅ Text extracted. Generating questions now...")

        for q_type, count in question_targets.items():
            if count > 0:
                st.subheader(f"📝 {q_type}")
                try:
                    questions = generate_questions_with_openai(all_text, q_type, count)
                    for i, q in enumerate(questions, 1):
                        st.markdown(f"**Q{i}:** {q.strip()}")
                except Exception as e:
                    st.error(f"❌ Error generating {q_type} questions: {e}")
