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

# --- GPT call helper ---
def gpt_call(prompt, max_tokens=500):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

# --- Extract topics from the document ---
def extract_topics(text):
    prompt = (
        "Bitte extrahiere aus dem folgenden Text maximal 7 wichtige Themen als kurze Stichwörter, "
        "kommagetrennt, ohne Beschreibung:\n\n"
        f"{text}\n\nThemen:"
    )
    topics_str = gpt_call(prompt, max_tokens=100)
    # Split by commas and strip spaces
    topics = [t.strip() for t in topics_str.split(",") if t.strip()]
    return topics[:7]

# --- Generate questions and keys ---
def generate_questions_with_keys(text, topic, num_questions, question_type, partial_points=None, max_length=None):
    # Build prompt based on question type
    base_prompt = f"Erstelle {num_questions} Fragen zum Thema '{topic}' basierend auf folgendem Text:\n\n{text}\n\n"
    
    if question_type == "Multiple Choice (einzelne Antwort)":
        prompt = (
            base_prompt +
            "Jede Frage soll 4 Antwortmöglichkeiten haben, von denen genau eine richtig ist. "
            "Bitte gib die Fragen und die richtige Antwort als Antwortschlüssel an."
        )
    elif question_type == "Multiple Choice (mehrere Antworten, Teilpunkte)":
        prompt = (
            base_prompt +
            "Jede Frage soll 4 Antwortmöglichkeiten haben, von denen mehrere richtig sein können. "
            f"Berücksichtige Teilpunkte (partial points) bei der Auswertung, mit folgendem Punkteschema: {partial_points}."
            "Bitte gib die Fragen und die richtigen Antworten als Antwortschlüssel an."
        )
    elif question_type == "Offene Fragen":
        prompt = (
            base_prompt +
            "Erstelle offene Fragen. "
            f"Die Antworten sollen maximal {max_length} Wörter lang sein. "
            "Bitte gib die Fragen und passende Antwortschlüssel an."
        )
    elif question_type == "Matching (Zuordnungen)":
        prompt = (
            base_prompt +
            "Erstelle Matching-Fragen, bei denen Begriffe zugeordnet werden sollen. "
            "Bitte gib die Fragen und die Lösungsschlüssel an."
        )
    else:
        prompt = base_prompt

    # Ask GPT for questions + answers
    response = gpt_call(prompt, max_tokens=1500)
    
    # Simple parsing: Assume format "Frage 1: ... Antwort: ..."
    # We will split by "Frage" and parse pairs
    q_and_a = []
    parts = response.split("Frage ")
    for part in parts[1:]:  # skip first split as it is before Frage 1
        try:
            q_part, a_part = part.split("Antwort", 1)
            question = q_part.strip(": .\n")
            answer = a_part.strip(": .\n")
            q_and_a.append((question, answer))
        except ValueError:
            # fallback: if no "Antwort" word found, take whole as question only
            q_and_a.append((part.strip(), ""))
    return q_and_a

# --- Streamlit App ---
st.title("Mehrfach-Fragentypen Generator mit Antwortschlüssel")

uploaded_file = st.file_uploader("Lade ein Textdokument hoch (.txt)", type=["txt"])

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    st.write("### Eingelesener Text (Vorschau):")
    st.write(text[:1000] + ("..." if len(text) > 1000 else ""))

    with st.spinner("Extrahiere Themen..."):
        topics = extract_topics(text)
    st.success("Themen extrahiert!")

    selected_topics = st.multiselect("Wähle ein oder mehrere Themen aus:", topics)
    question_types = st.multiselect(
        "Wähle einen oder mehrere Fragetypen aus:",
        [
            "Multiple Choice (einzelne Antwort)",
            "Multiple Choice (mehrere Antworten, Teilpunkte)",
            "Offene Fragen",
            "Matching (Zuordnungen)",
        ],
    )

    num_questions = st.slider("Anzahl der Fragen pro Thema und Fragetyp", 1, 10, 3)
    partial_points = None
    max_length = None

    if "Multiple Choice (mehrere Antworten, Teilpunkte)" in question_types:
        partial_points = st.text_input(
            "Punkteschema für Multiple Choice mit Teilpunkten (z.B. 2-1-0 für richtig - teilweise richtig - falsch)",
            value="2-1-0",
        )
    if "Offene Fragen" in question_types:
        max_length = st.number_input(
            "Maximale Länge der Antwort bei offenen Fragen (Wörter)",
            min_value=10,
            max_value=200,
            value=50,
        )

    if st.button("Fragen generieren"):
        if not selected_topics:
            st.error("Bitte wähle mindestens ein Thema aus.")
        elif not question_types:
            st.error("Bitte wähle mindestens einen Fragetyp aus.")
        else:
            all_questions_text = ""
            for topic in selected_topics:
                st.header(f"Thema: {topic}")
                all_questions_text += f"== Thema: {topic} ==\n\n"
                for q_type in question_types:
                    st.subheader(f"Fragetyp: {q_type}")
                    with st.spinner(f"Generiere Fragen für Thema '{topic}' - {q_type}..."):
                        q_and_a = generate_questions_with_keys(
                            text,
                            topic,
                            num_questions,
                            q_type,
                            partial_points=partial_points,
                            max_length=max_length,
                        )
                    for idx, (q, a) in enumerate(q_and_a, 1):
                        st.markdown(f"**Frage {idx}:** {q}")
                        st.markdown(f"**Antwort:** {a}")
                        all_questions_text += f"Frage {idx}: {q}\nAntwort: {a}\n\n"

            # Download button for all questions + answers
            st.download_button(
                label="Alle Fragen & Antwortschlüssel herunterladen",
                data=all_questions_text,
                file_name="fragen_antworten.txt",
                mime="text/plain",
            )
")
