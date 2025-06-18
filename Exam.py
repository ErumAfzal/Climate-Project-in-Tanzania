import streamlit as st
from typing import List
import fitz  # PyMuPDF
import json
import pandas as pd

def extract_text_from_pdf(file) -> str:
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
    doc_excerpt = "\n---\n".join(documents_text) if documents_text else "Keine Dokumente hochgeladen."
    qtypes_str = ", ".join(question_types) if question_types else "Mehrfachauswahl (MCQ)"

    # Important: Force Wahr/Falsch to have 4 options, others normal.
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

Bitte gib die Fragen ausschließlich als gültiges JSON zurück, das folgendes Schema erfüllt:

[
 {{
  "frage": "Frage hier",
  "antworten": ["Antwort A", "Antwort B", "Antwort C", "Antwort D"],
  "richtige_antwort": "Antwort B",
  "typ": "MCQ" | "Wahr/Falsch" | "Offen" | "Matching"
 }},
 ...
]

Wichtig:
- Wenn "typ" = "Wahr/Falsch", müssen genau 4 Antwortmöglichkeiten generiert werden (z.B. "Wahr", "Falsch" und zwei weitere plausible Optionen).
- Für offene Fragen ("Offen") nur "frage" und "typ" angeben, ohne Antwortmöglichkeiten.
- Generiere keine zusätzliche Erklärung, nur das reine JSON-Array.

Beginne jetzt mit der Generierung.
"""
    return prompt

def call_openai_api(api_key: str, prompt: str) -> str:
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

def validate_and_format_questions(raw_text: str):
    """Try to parse JSON and return list, else None and raw text."""
    try:
        questions = json.loads(raw_text)
        if not isinstance(questions, list):
            return None, raw_text
        # Check Wahr/Falsch questions for 4 options
        for q in questions:
            if q.get("typ") == "Wahr/Falsch":
                antworten = q.get("antworten", [])
                if len(antworten) != 4:
                    # Fix by adding dummy options if less than 4
                    while len(antworten) < 4:
                        antworten.append("Option " + chr(65 + len(antworten)))  # Option A,B,C,D
                    q["antworten"] = antworten[:4]
        return questions, None
    except json.JSONDecodeError:
        return None, raw_text

def questions_to_text(questions: List[dict]) -> str:
    """Format questions nicely to copy-paste text."""
    lines = []
    for i, q in enumerate(questions, start=1):
        lines.append(f"Frage {i}: {q.get('frage','')}")
        antworten = q.get("antworten", [])
        if antworten:
            for idx, a in enumerate(antworten):
                prefix = chr(65 + idx) + ")"
                lines.append(f"  {prefix} {a}")
        richtige = q.get("richtige_antwort", "")
        if richtige:
            lines.append(f"Richtige Antwort: {richtige}")
        lines.append(f"Typ: {q.get('typ','')}")
        lines.append("")  # blank line between questions
    return "\n".join(lines)

def json_to_dataframe(questions: List[dict]) -> pd.DataFrame:
    rows = []
    for q in questions:
        antworten = q.get("antworten", [])
        antworten_str = " | ".join(antworten) if antworten else ""
        rows.append(
            {
                "Frage": q.get("frage", ""),
                "Antworten": antworten_str,
                "Richtige Antwort": q.get("richtige_antwort", ""),
                "Typ": q.get("typ", ""),
            }
        )
    return pd.DataFrame(rows)

def main():
    st.title("EQF 6 Prüfungsfragen Generator (Deutsch)")

    st.markdown(
        """
        Dieses Tool erzeugt hochwertige Prüfungsfragen auf dem Niveau EQF 6 basierend auf hochgeladenen Dokumenten und Beispiel-Fragen.
        """
    )

    api_key = st.text_input(
        "OpenAI API Key eingeben", type="password", placeholder="sk-...", help="Benötigt für die Fragegenerierung"
    )
    if not api_key:
        st.warning("Bitte gib deinen OpenAI API Key ein, um fortzufahren.")
        st.stop()

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

    uploaded_files = st.file_uploader(
        "Bis zu 3 Dokumente hochladen (PDF, Text)", type=["pdf", "txt"], accept_multiple_files=True
    )
    if uploaded_files and len(uploaded_files) > 3:
        st.warning("Bitte lade maximal 3 Dokumente hoch.")
        uploaded_files = uploaded_files[:3]

    documents_text = []
    if uploaded_files:
        for file in uploaded_files:
            if file.type == "application/pdf":
                text = extract_text_from_pdf(file)
            else:
                text = file.read().decode("utf-8")
            documents_text.append(text)

    sample_questions = st.text_area(
        "Beispielhafte Prüfungsfragen (auf Deutsch) einfügen",
        height=150,
        placeholder="Hier Beispiel-Fragen im deutschen EQF 6 Stil einfügen...",
    )

    question_types = st.multiselect(
        "Fragetypen auswählen",
        options=["MCQ", "Matching", "Offene Fragen", "Wahr/Falsch"],
        default=["MCQ"],
        help="Welche Fragetypen sollen generiert werden?",
    )

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
            raw_result = call_openai_api(api_key, prompt)
            questions, raw_error = validate_and_format_questions(raw_result)

            if questions:
                st.success("Fragen erfolgreich generiert!")

                df = json_to_dataframe(questions)
                st.dataframe(df)

                # Show text area for easy copy-paste with answer keys
                readable_text = questions_to_text(questions)
                st.text_area("Generierte Fragen (kopieren Sie hier die Fragen mit Antwortschlüssel)", readable_text, height=400)

                # Download options
                csv = df.to_csv(index=False).encode("utf-8")
                json_output = json.dumps(questions, ensure_ascii=False, indent=2).encode("utf-8")
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
                st.error("Die generierten Fragen sind kein gültiges JSON.")
                st.text_area("Rohantwort von OpenAI (zum Debuggen)", raw_error, height=300)

    st.markdown("---")
    st.markdown(
        "© 2025 Erum Afzal | Powered by OpenAI GPT und Streamlit"
    )

if __name__ == "__main__":
    main()
