import streamlit as st
import openai
from PyPDF2 import PdfReader
from docx import Document
from io import StringIO
import datetime

# --- Streamlit page configuration ---
st.set_page_config(page_title="EQF 6–7 Fragen-Generator (Deutsch)", layout="wide")
st.title("🎓 EQF 6–7 Fragen-Generator für Lehrerbildung (Deutsch)")

# --- OpenAI API Key ---
api_key = st.text_input("🔑 OpenAI API-Schlüssel eingeben", type="password")
if api_key:
    openai.api_key = api_key
else:
    st.warning("Bitte API-Schlüssel eingeben, um fortzufahren.")
    st.stop()

# --- File reading functions ---
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    elif file.name.endswith(".docx"):
        return extract_text_from_docx(file)
    else:
        return file.read().decode("utf-8")

# --- Topic and format configuration ---
topics = {
    "Teil 1: Arbeiten in multiprofessionellen Teams / Ganztagsschule": 8,
    "Teil 2: Bildung und Ungleichheit": 8,
    "Teil 3: INTER_A": 5,
    "Teil 4: Interdisziplinäres Lernen": 8,
    "Teil 5: Kommunikation und kommunikative Kompetenzen": 8,
}

selected_topics = st.multiselect("🧠 Wähle die Themenbereiche", list(topics.keys()), default=list(topics.keys()))

question_type = st.selectbox("📝 Frageformat wählen", ["Gemischt", "Offene Fragen", "Multiple Choice", "Fallbasiert"])

question_type_instruction = {
    "Gemischt": "",
    "Offene Fragen": "Es sollen ausschließlich offene Fragen sein.",
    "Multiple Choice": "Es sollen ausschließlich Multiple-Choice-Fragen mit je vier Antwortmöglichkeiten und einer richtigen Antwort sein.",
    "Fallbasiert": "Die Fragen sollen auf kurzen Unterrichts- oder Alltagssituationen basieren (Fallvignetten)."
}[question_type]

uploaded_files = st.file_uploader("📂 Lade deine Literatur hoch (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"], accept_multiple_files=True)

# --- Question Generator ---
def generate_questions(text, topic_title, question_count):
    system_prompt = (
        "Du bist ein Bildungsexperte, der Fragen auf EQF-Niveau 6–7 erstellt. "
        "Berücksichtige relevante Bildungstheorien, reale Unterrichtssituationen und "
        "eine wissenschaftliche Tiefe. Verwende eine akademische Sprache auf Deutsch. "
        f"Jede Frage muss thematisch zum folgenden Bereich passen: '{topic_title}'"
    )

    user_prompt = (
        f"Generiere bitte {question_count} akademische Prüfungsfragen (offen oder MC) zum Thema '{topic_title}'. "
        f"{question_type_instruction} Verwende den folgenden deutschen Inhalt zur Inspiration:\n\n"
        f"{text[:4000]}\n\n"
        "Die Fragen sollen geeignet für Lehramtsstudierende auf Master-Niveau sein, Theorie und Praxis verbinden "
        "und kritisch-reflexives Denken fördern."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4,
        max_tokens=1800
    )

    return response.choices[0].message.content.strip().split("\n\n")

# --- Generate Button ---
if st.button("🚀 Fragen generieren"):
    if not uploaded_files:
        st.warning("⚠️ Bitte lade mindestens eine Literaturdatei hoch.")
        st.stop()

    with st.spinner("📚 Texte werden verarbeitet..."):
        combined_text = "\n\n".join([extract_text(f) for f in uploaded_files])

    all_questions = []

    for topic in selected_topics:
        count = topics[topic]
        st.markdown(f"## 🧠 {topic}")
        try:
            questions = generate_questions(combined_text, topic, count)
            for i, q in enumerate(questions, 1):
                st.markdown(f"**Frage {i}:** {q.strip()}")
                all_questions.append(f"{topic} - Frage {i}:\n{q.strip()}\n")
        except Exception as e:
            st.error(f"❌ Fehler bei der Generierung von Fragen für {topic}: {e}")

    # --- Download as text file ---
    if all_questions:
        output_text = "\n".join(all_questions)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"EQF_Fragentext_{timestamp}.txt"
        st.download_button("💾 Fragen als TXT herunterladen", data=output_text, file_name=filename, mime="text/plain")
