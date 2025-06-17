import streamlit as st
import openai
from PyPDF2 import PdfReader
from docx import Document
import datetime

# --- Page config ---
st.set_page_config(page_title="EQF 6–7 Fragen-Generator (Deutsch)", layout="wide")
st.title("🎓 EQF 6–7 Fragen-Generator für Lehrerbildung (Deutsch)")

# --- API key input ---
api_key = st.text_input("🔑 OpenAI API-Schlüssel eingeben", type="password")
if api_key:
    openai.api_key = api_key
else:
    st.warning("Bitte API-Schlüssel eingeben, um fortzufahren.")
    st.stop()

# --- Text extraction functions ---
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    texts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            texts.append(text)
    return "\n".join(texts)

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

# --- Topics & default question counts ---
topics = {
    "Teil 1: Arbeiten in multiprofessionellen Teams / Ganztagsschule": 8,
    "Teil 2: Bildung und Ungleichheit": 8,
    "Teil 3: INTER_A": 5,
    "Teil 4: Interdisziplinäres Lernen": 8,
    "Teil 5: Kommunikation und kommunikative Kompetenzen": 8,
}

# --- UI: Select topics ---
selected_topics = st.multiselect("🧠 Wähle die Themenbereiche", list(topics.keys()), default=list(topics.keys()))

# --- UI: Select question types ---
question_types_available = ["Multiple Choice (einzelne Antwort)", "Multiple Choice (mehrere Antworten, Teilpunkte)", "Offene Fragen", "Matching (Zuordnungen)"]
question_type = st.selectbox("📝 Frageformat wählen", question_types_available)

# --- UI: Number of questions ---
num_questions = st.number_input("Wie viele Fragen pro Thema generieren?", min_value=1, max_value=20, value=5, step=1)

# --- UI: Question-type-specific settings ---
if question_type.startswith("Multiple Choice"):
    st.markdown("**MC Einstellungen:**")
    if question_type == "Multiple Choice (mehrere Antworten, Teilpunkte)":
        partial_points = st.number_input("Teilpunktwert pro richtige Antwortoption (z.B. 0.5)", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    else:
        partial_points = None
elif question_type == "Offene Fragen":
    max_length = st.number_input("Maximale Antwortlänge (Zeichen), 0 für unbegrenzt", min_value=0, max_value=1000, value=0, step=50)
else:
    partial_points = None
    max_length = None

# --- Upload literature ---
uploaded_files = st.file_uploader("📂 Lade deine Literatur hoch (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"], accept_multiple_files=True)

# --- OpenAI question generator function ---
def generate_questions(text, topic_title, question_count, q_type, partial_points=None, max_length=None):
    # Base prompt for question generation
    system_prompt = (
        "Du bist ein Bildungsexperte, der Prüfungsfragen auf EQF-Niveau 6–7 erstellt. "
        "Berücksichtige relevante Bildungstheorien, reale Unterrichtssituationen und eine wissenschaftliche Tiefe. "
        f"Erzeuge {question_count} Fragen zum Thema '{topic_title}' im folgenden Format."
    )
    
    # Define instructions depending on question type
    if q_type == "Multiple Choice (einzelne Antwort)":
        type_instruction = (
            "Erzeuge Multiple-Choice-Fragen mit genau 4 Antwortmöglichkeiten, von denen genau eine korrekt ist. "
            "Kennzeichne die richtige Antwort klar."
        )
    elif q_type == "Multiple Choice (mehrere Antworten, Teilpunkte)":
        type_instruction = (
            "Erzeuge Multiple-Choice-Fragen mit 4 Antwortmöglichkeiten, von denen mehrere richtig sein können. "
            f"Ordne jeder richtigen Antwort eine Teilpunktzahl von {partial_points} zu. "
            "Kennzeichne alle korrekten Antworten deutlich."
        )
    elif q_type == "Offene Fragen":
        length_note = f" Die Antwort darf maximal {max_length} Zeichen lang sein." if max_length and max_length > 0 else " Die Antwortlänge ist unbegrenzt."
        type_instruction = f"Erzeuge offene Fragen ohne Antwortoptionen.{length_note}"
    elif q_type == "Matching (Zuordnungen)":
        type_instruction = (
            "Erzeuge Matching-Fragen mit klar definierten Paaren zum Zuordnen, z.B. Begriff und Definition. "
            "Erstelle 5 Paare pro Frage."
        )
    else:
        type_instruction = ""

    user_prompt = (
        f"{type_instruction}\n"
        "Die Fragen sollen auf Deutsch sein, keine Duplikate enthalten, akademisch formuliert sein, "
        "und für Lehramtsstudierende auf Master-Niveau geeignet sein, Theorie und Praxis verbindend.\n\n"
        f"Verwende diesen Text als Quelle zur Inspiration:\n\n{text[:4000]}"
    )
    
    # Call OpenAI ChatCompletion
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
            max_tokens=1800
        )
    except Exception as e:
        st.error(f"OpenAI API-Fehler: {e}")
        return []

    # Basic parsing: split by double newlines to separate questions
    questions_raw = response.choices[0].message.content.strip().split("\n\n")
    questions = [q.strip() for q in questions_raw if len(q.strip()) > 20]
    return questions

# --- Generate button and question output ---
if st.button("🚀 Fragen generieren"):
    if not uploaded_files:
        st.warning("⚠️ Bitte lade mindestens eine Literaturdatei hoch.")
        st.stop()

    with st.spinner("📚 Literaturtexte werden verarbeitet..."):
        combined_text = "\n\n".join([extract_text(f) for f in uploaded_files])

    all_questions = []

    for topic in selected_topics:
        st.markdown(f"## 🧠 Thema: {topic}")
        try:
            qs = generate_questions(
                combined_text,
                topic,
                num_questions,
                question_type,
                partial_points=partial_points if 'partial_points' in locals() else None,
                max_length=max_length if 'max_length' in locals() else None,
            )
            if not qs:
                st.warning(f"Keine Fragen generiert für {topic}.")
                continue
            for i, question in enumerate(qs, 1):
                st.markdown(f"**Frage {i}:** {question}")
                all_questions.append(f"{topic} - Frage {i}:\n{question}\n")
            st.markdown(f"*Insgesamt {len(qs)} Fragen für '{topic}' generiert.*")
        except Exception as e:
            st.error(f"❌ Fehler bei der Generierung von Fragen für {topic}: {e}")

    # Download generated questions as text file
    if all_questions:
        output_text = "\n".join(all_questions)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"EQF_Exam_{timestamp}.txt"
        st.download_button("💾 Fragen als TXT herunterladen", data=output_text, file_name=filename, mime="text/plain")
