import streamlit as st
from typing import List, Dict
import fitz  # PyMuPDF
import os
import tempfile
import json
import pandas as pd
from io import StringIO
from openai import OpenAI
from openai.error import OpenAIError

# Initialize OpenAI client placeholder (we will use openai.ChatCompletion later)
# User inputs API key in app


def extract_text_from_pdf(file) -> str:
    """Extract text from PDF file using PyMuPDF."""
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        st.error(f"PDF extraction error: {e}")
        return ""


def prepare_prompt(
    section: str,
    documents_text: List[str],
    sample_questions: str,
    question_types: List[str],
    number_of_questions: int,
) -> str:
    """Create prompt for OpenAI question generation."""

    doc_excerpt = "\n---\n".join(documents_text) if documents_text else "Keine Dokumente hochgeladen."
    qtypes_str = ", ".join(question_types) if question_types else "Mehrfachauswahl (MCQ)"

    prompt = f"""
Du bist ein Experte für Bildungswissenschaften und erstellst Prüfungsfragen auf dem Niveau des EQF 6 (Fachhochschulniveau).

Arbeite mit folgenden Vorgaben:

Abschnitt/Thema: {section}

Verfügbare Dokumente (Auszüge): 
{doc_excerpt}

Beispielhafte Beispiel-Fragen, die als Format dienen:
{sample_questions}

Erstelle nun bitte {number_of_questions} hochwertige Prüfungsfragen, die folgende Fragearten enthalten: {qtypes_str}.

Jede Frage sollte im Kontext der hochgeladenen Dokumente stehen und möglichst konkrete Textstellen oder Begriffe daraus referenzieren.

Bitte gib die Fragen mit Antwortmöglichkeiten (falls MCQ) und Antwortschlüsseln zurück, strukturiert als JSON-Array mit folgendem Schema:

[
 {{
  "frage": "Frage hier",
  "antworten": ["Antwort A", "Antwort B", "Antwort C", "Antwort D"],
  "richtige_antwort": "Antwort B",
  "typ": "MCQ"
 }},
 ...
]

Falls offene Fragen, dann nur "frage" und "typ": "Offen".

Beginne jetzt mit der Generierung.
"""
    return prompt


def call_openai_api(api_key: str, prompt: str) -> str:
    """Call OpenAI Chat Completion with given prompt."""
    try:
        import openai

        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Du bist ein hilfreicher Assistent für Bildungsfragen."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1500,
            n=1,
        )
        return response.choices[0].message.content.strip()
    except OpenAIError as e:
        st.error(f"OpenAI API Fehler: {e}")
        return ""
    except Exception as e:
        st.error(f"Unbekannter Fehler bei API-Aufruf: {e}")
        return ""


def json_to_dataframe(questions_json: str) -> pd.DataFrame:
    """Convert questions JSON string to pandas DataFrame for display."""

    try:
        questions = json.loads(questions_json)
        rows = []
        for q in questions:
            antworten = q.get("antworten", [])
            antworten_str = " | ".join(antworten) if antworten else ""
            richtige_antwort = q.get("richtige_antwort", "")
            rows.append(
                {
                    "Frage": q.get("frage", ""),
                    "Antworten": antworten_str,
                    "Richtige Antwort": richtige_antwort,
                    "Typ": q.get("typ", ""),
                }
            )
        df = pd.DataFrame(rows)
        return df
    except json.JSONDecodeError:
        st.warning("Die generierten Fragen sind kein gültiges JSON.")
        return pd.DataFrame()


def main():
    st.title("EQF 6 Prüfungsfragen Generator (Deutsch)")

    st.markdown(
        """
        Dieses Tool erzeugt hochwertige Prüfungsfragen auf dem Niveau EQF 6 basierend auf hochgeladenen Dokumenten und Beispiel-Fragen.
        """
    )

    # API key input
    api_key = st.text_input(
        "OpenAI API Key eingeben", type="password", placeholder="sk-...", help="Benötigt für die Fragegenerierung"
    )
    if not api_key:
        st.warning("Bitte gib deinen OpenAI API Key ein, um fortzufahren.")
        st.stop()

    # Section selector
    section = st.selectbox(
        "Abschnitt / Modul auswählen",
        options=[
            "Bildung und Ungleichheit",
            "Demokratische Bildung",
            "Ganztagsschule",
            "INTER A - Bildungsforschung",
            "Kommunikation und Kommunikative Fähigkeiten",
        ],
    )

    # File uploader (up to 3)
    uploaded_files = st.file_uploader(
        "Bis zu 3 Dokumente hochladen (PDF, Text)", type=["pdf", "txt"], accept_multiple_files=True, key="doc_upload"
    )
    if uploaded_files and len(uploaded_files) > 3:
        st.warning("Bitte lade maximal 3 Dokumente hoch.")
        uploaded_files = uploaded_files[:3]

    # Extract text from uploaded docs
    documents_text = []
    if uploaded_files:
        for file in uploaded_files:
            if file.type == "application/pdf":
                text = extract_text_from_pdf(file)
            else:
                text = file.read().decode("utf-8")
            documents_text.append(text)

    # Sample questions input
    sample_questions = st.text_area(
        "Beispielhafte Prüfungsfragen (auf Deutsch) einfügen",
        height=150,
        placeholder="Hier Beispiel-Fragen im deutschen EQF 6 Stil einfügen...",
    )

    # Question types multi-select
    question_types = st.multiselect(
        "Fragetypen auswählen",
        options=["MCQ", "Matching", "Offene Fragen", "Wahr/Falsch"],
        default=["MCQ"],
        help="Welche Fragetypen sollen generiert werden?",
    )

    # Number of questions
    number_of_questions = st.number_input(
        "Anzahl der zu generierenden Fragen",
        min_value=1,
        max_value=50,
        value=10,
        step=1,
    )

    if st.button("Fragen generieren"):
        with st.spinner("Generiere Fragen..."):
            prompt = prepare_prompt(section, documents_text, sample_questions, question_types, number_of_questions)
            result = call_openai_api(api_key, prompt)

            if result:
                st.success("Fragen erfolgreich generiert!")

                df = json_to_dataframe(result)
                if not df.empty:
                    st.dataframe(df)
                    # Download options
                    csv = df.to_csv(index=False).encode("utf-8")
                    json_output = result.encode("utf-8")
                    st.download_button(
                        label="Fragen als CSV herunterladen",
                        data=csv,
                        file_name=f"eqf6_questions_{section}.csv",
                        mime="text/csv",
                    )
                    st.download_button(
                        label="Fragen als JSON herunterladen",
                        data=json_output,
                        file_name=f"eqf6_questions_{section}.json",
                        mime="application/json",
                    )
                else:
                    st.warning("Keine Fragen zum Anzeigen gefunden.")
            else:
                st.error("Fehler bei der Fragegenerierung.")

    st.markdown("---")
    st.markdown(
        "© 2025 Erum Afzal | Powered by OpenAI GPT und Streamlit"
    )


if __name__ == "__main__":
    main()
