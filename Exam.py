import streamlit as st
import openai
from PyPDF2 import PdfReader
import re

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def read_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return ""
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    else:
        # Assume text/plain
        return str(uploaded_file.read(), "utf-8")

def parse_sample_questions(sample_text):
    """
    Analyze sample questions text to get question types and option counts.
    This is a simplified heuristic parser based on your sample format.
    Returns a list of dicts:
    [{ 'question_type': 'single_choice' or 'multiple_choice' or 'matching',
       'num_options': int,
       'points': float
     }, ...]
    """
    questions = []
    # Split by "Frage" to get each question block
    blocks = re.split(r"Frage\s*\d+", sample_text)
    for block in blocks:
        if len(block.strip()) < 10:
            continue
        # Count options by looking for lines with option pattern "Die ... (" or capital letter + parenthesis
        options = re.findall(r"^[A-ZÄÖÜ].+[(]", block, flags=re.MULTILINE)
        num_options = len(options)
        # Points heuristic: look for "(x Punkt)" or (x Punkte)
        points_match = re.search(r"\(([\d\.]+) Punkt", block)
        points = float(points_match.group(1)) if points_match else 1.0

        # Check if multiple answers can be selected: if multiple options have (Ausgewählt = x Punkte)
        multi_select = "Ausgewählt" in block and block.count("Ausgewählt") > 1

        qtype = "multiple_choice" if multi_select else "single_choice"

        # Matching could be inferred by presence of "Ordnen Sie ... zu" or similar
        if "Ordnen Sie" in block or "Zuordnung" in block:
            qtype = "matching"

        questions.append({
            "question_type": qtype,
            "num_options": num_options if num_options > 0 else 4,  # fallback to 4
            "points": points
        })
    return questions

def build_prompt(doc_text, question_style, question_num, exam_set_num):
    """
    Build a prompt for OpenAI API to generate a question.

    Parameters:
    - doc_text: text content from the uploaded documents
    - question_style: dict with keys 'question_type' and 'num_options'
    - question_num: int question index for exam set
    - exam_set_num: which exam set (1 or 2)

    Returns a string prompt in German instructing the model to generate
    an original EQF 6-7 question from the content, matching style.
    """
    qtype = question_style['question_type']
    num_opts = question_style['num_options']

    prompt = f"""
Du bist ein erfahrener Entwickler und Sozialwissenschaftler mit Doktortitel. Du sollst eine hochqualitative Prüfungsfrage auf Deutsch erstellen für die EQF Stufe 6–7 basierend auf folgendem Dokumentinhalt:

'''{doc_text[:3000]}'''

Die Frage soll originell sein und darf keine Duplikate oder Paraphrasen aus bereits gegebenen Musterfragen enthalten. Verwende akademische, präzise Sprache auf hohem Niveau.

Frage {question_num} aus Prüfungsset {exam_set_num}:

Erstelle eine { 'Mehrfachauswahlfrage' if qtype == 'multiple_choice' else ('Zuordnungsfrage' if qtype == 'matching' else 'Einzelauswahlfrage')} mit genau {num_opts} Antwortoptionen.

Bitte schreibe die Frage in folgendem Format:

Frage {question_num} - EQF 6–7 - Prüfungsset {exam_set_num}

[Fragentext]

A) [Option A]
B) [Option B]
C) [Option C]
{ 'D) [Option D]' if num_opts>=4 else '' }
{ 'E) [Option E]' if num_opts>=5 else '' }
{ 'F) [Option F]' if num_opts==6 else '' }

Markiere die richtige(n) Antwort(en) und gib für jede Option an, wie viele Punkte (zwischen 0 und 1) sie bringt, so dass die Gesamtsumme der Punkte 1 ergibt. Verwende dabei Punktzahlen mit 2 Dezimalstellen.

Erstelle außerdem eine kurze Erklärung, warum die richtige Antwort korrekt ist.

Beantworte ausschließlich in diesem Format. Keine weiteren Kommentare.
"""
    return prompt

def generate_question(openai_api_key, prompt):
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Du bist ein hilfsbereiter Assistent für die Erstellung von Prüfungsfragen auf Deutsch."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=700,
        n=1,
        stop=None,
    )
    return response.choices[0].message.content.strip()

st.title("EQF 6–7 Prüfungsfragen-Generator für Lehrerbildung (Deutsch)")

st.markdown("""
Dieses Tool generiert zwei Sets von hochwertigen Prüfungsfragen basierend auf deinen hochgeladenen Dokumenten und einem Satz von Musterfragen.
- Lade deine Musterfragen-Datei hoch (txt oder pdf)
- Lade 3 Dokumente hoch, aus denen die Fragen generiert werden sollen (txt oder pdf)
- Gib deinen OpenAI API Schlüssel ein
- Erhalte zwei vollständige Prüfungssätze mit Fragen, Antwortoptionen und Antwortschlüsseln
""")

api_key = st.text_input("OpenAI API Schlüssel", type="password")

sample_file = st.file_uploader("Musterfragen Datei (txt oder pdf)", type=["txt", "pdf"])

doc_files = st.file_uploader("3 Quelldokumente (txt oder pdf, mehrere auswählen)", type=["txt", "pdf"], accept_multiple_files=True)

generate_btn = st.button("2 Prüfungssets generieren")

if generate_btn:
    if not api_key:
        st.error("Bitte gib deinen OpenAI API Schlüssel ein.")
    elif not sample_file:
        st.error("Bitte lade deine Musterfragen-Datei hoch.")
    elif len(doc_files) < 3:
        st.error("Bitte lade genau 3 Quelldokumente hoch.")
    else:
        with st.spinner("Lade und analysiere Dateien..."):
            sample_text = read_uploaded_file(sample_file)
            docs_text = ""
            for f in doc_files:
                docs_text += read_uploaded_file(f) + "\n\n"

            st.success("Dateien erfolgreich geladen.")

            question_styles = parse_sample_questions(sample_text)
            if len(question_styles) < 5:
                st.warning("Wenig Fragen im Muster. Es wird mit 5 Standardfragen gearbeitet.")
                question_styles = [
                    {"question_type": "single_choice", "num_options": 4, "points": 1},
                    {"question_type": "multiple_choice", "num_options": 4, "points": 3},
                    {"question_type": "single_choice", "num_options": 6, "points": 1},
                    {"question_type": "matching", "num_options": 3, "points": 3},
                    {"question_type": "single_choice", "num_options": 4, "points": 1},
                ]

            # Generate 2 exam sets with half questions each
            num_questions = len(question_styles)
            exam1_styles = question_styles[:num_questions//2]
            exam2_styles = question_styles[num_questions//2:]

            st.markdown("### Prüfungsset 1")
            for i, qs in enumerate(exam1_styles, 1):
                prompt = build_prompt(docs_text, qs, i, 1)
                question = generate_question(api_key, prompt)
                st.markdown(question)
                st.write("---")

            st.markdown("### Prüfungsset 2")
            for i, qs in enumerate(exam2_styles, 1):
                prompt = build_prompt(docs_text, qs, i, 2)
                question = generate_question(api_key, prompt)
                st.markdown(question)
                st.write("---")
