import streamlit as st
from io import BytesIO
import speech_recognition as sr

# === Language packs ===
LANG_DATA = {
    "EN": {
        "title": "Teacher-Principal Role-Play Chatbot",
        "select_language": "Select Language",
        "select_scenario": "Select Scenario",
        "scenario_strategic": "Strategic Communication",
        "scenario_understanding": "Understanding-Oriented Communication",
        "select_input": "Select Input Type",
        "input_text": "Text Input",
        "input_audio": "Audio Input",
        "instructions_title": "Teacher Instructions",
        "start_conversation": "Start Conversation",
        "type_message": "Type your message here...",
        "record_audio": "Record your question and click 'Send'",
        "send": "Send",
        "conversation_log": "Conversation Log",
        "role_teacher": "You (Teacher - Ms. Blum):",
        "role_principal": "Principal (AI - Ms. Ziegler):",
        "no_audio": "No audio input detected. Please try again.",
        "listening": "Listening... Please speak.",
        "error_audio": "Sorry, could not recognize audio. Please try again.",
        "scenario_desc": {
            "Strategic Communication": (
                "In this scenario, the Principal (Ms. Ziegler) will respond "
                "with a focus on strategic communication — emphasizing school policies, "
                "goals, and managing concerns tactfully."
            ),
            "Understanding-Oriented Communication": (
                "In this scenario, the Principal (Ms. Ziegler) will respond with "
                "empathy, acknowledging the teacher’s feelings and focusing on mutual understanding."
            ),
        },
        "instructions_teacher": (
            "You are Ms. Blum, a teacher discussing feedback culture with your principal. "
            "Express concerns about the current feedback criteria and seek dialogue."
        ),
    },
    "DE": {
        "title": "Lehrer-Schulleiter Rollenspiel Chatbot",
        "select_language": "Sprache wählen",
        "select_scenario": "Szenario wählen",
        "scenario_strategic": "Strategische Kommunikation",
        "scenario_understanding": "Verständnisorientierte Kommunikation",
        "select_input": "Eingabetyp wählen",
        "input_text": "Texteingabe",
        "input_audio": "Audioeingabe",
        "instructions_title": "Anleitung für Lehrer*innen",
        "start_conversation": "Gespräch starten",
        "type_message": "Hier Nachricht eingeben...",
        "record_audio": "Nehmen Sie Ihre Frage auf und klicken Sie 'Senden'",
        "send": "Senden",
        "conversation_log": "Gesprächsverlauf",
        "role_teacher": "Sie (Lehrer*in - Frau Blum):",
        "role_principal": "Schulleiterin (KI - Frau Ziegler):",
        "no_audio": "Keine Audioeingabe erkannt. Bitte versuchen Sie es erneut.",
        "listening": "Höre zu... Bitte sprechen.",
        "error_audio": "Entschuldigung, konnte Audio nicht erkennen. Bitte versuchen Sie es erneut.",
        "scenario_desc": {
            "Strategische Kommunikation": (
                "In diesem Szenario antwortet die Schulleiterin (Frau Ziegler) "
                "mit Fokus auf strategische Kommunikation – betont Schulpolitik, "
                "Ziele und taktvollen Umgang mit Bedenken."
            ),
            "Verständnisorientierte Kommunikation": (
                "In diesem Szenario antwortet die Schulleiterin (Frau Ziegler) "
                "einfühlsam, erkennt die Gefühle der Lehrkraft an und legt Wert auf gegenseitiges Verständnis."
            ),
        },
        "instructions_teacher": (
            "Sie sind Frau Blum, eine Lehrerin, die mit der Schulleiterin über Feedbackkultur spricht. "
            "Äußern Sie Ihre Bedenken zu den aktuellen Feedbackkriterien und suchen Sie den Dialog."
        ),
    },
}

# === Sample AI response templates aligned to scenarios ===
AI_RESPONSES = {
    "EN": {
        "Strategic Communication": [
            "I understand your concerns, Ms. Blum. However, the feedback criteria were designed to ensure consistency and fairness across all lessons.",
            "We must consider the school's overall goals and maintain high standards, even if some external factors vary.",
            "If the class size or tools pose difficulties, these can be discussed separately in future meetings to adjust support.",
            "This feedback culture is about improving quality and accountability, not punishment.",
            "Your suggestions for a checklist are noted. We'll aim to include framework conditions where feasible.",
        ],
        "Understanding-Oriented Communication": [
            "Thank you for sharing your concerns so openly, Ms. Blum. I appreciate your perspective on the broader teaching conditions.",
            "I recognize that each class and situation is unique, and that feedback should consider those nuances.",
            "It's important that we support you, not just evaluate you, and that the criteria feel fair to everyone.",
            "Maybe together we can develop a more holistic feedback approach that reflects these real challenges.",
            "Your idea of co-creating a checklist sounds like a great step to ensure everyone feels heard.",
        ],
    },
    "DE": {
        "Strategische Kommunikation": [
            "Ich verstehe Ihre Bedenken, Frau Blum. Die Feedback-Kriterien wurden jedoch entwickelt, um Konsistenz und Fairness in allen Unterrichtsstunden zu gewährleisten.",
            "Wir müssen die Gesamtziele der Schule berücksichtigen und hohe Standards aufrechterhalten, auch wenn externe Faktoren variieren.",
            "Wenn Klassengröße oder Hilfsmittel Schwierigkeiten bereiten, können diese in zukünftigen Sitzungen besprochen werden, um Unterstützung anzupassen.",
            "Diese Feedback-Kultur dient der Qualitätsverbesserung und Verantwortlichkeit, nicht als Bestrafung.",
            "Ihre Vorschläge für eine Checkliste sind notiert. Wir werden versuchen, Rahmenbedingungen wo möglich zu berücksichtigen.",
        ],
        "Verständnisorientierte Kommunikation": [
            "Vielen Dank, dass Sie Ihre Bedenken so offen geteilt haben, Frau Blum. Ich schätze Ihre Sicht auf die umfassenderen Unterrichtsbedingungen.",
            "Ich erkenne an, dass jede Klasse und Situation einzigartig ist und dass Feedback diese Nuancen berücksichtigen sollte.",
            "Es ist wichtig, Sie zu unterstützen und nicht nur zu bewerten, und dass die Kriterien sich für alle fair anfühlen.",
            "Vielleicht können wir gemeinsam einen ganzheitlicheren Feedback-Ansatz entwickeln, der diese realen Herausforderungen widerspiegelt.",
            "Ihre Idee, eine Checkliste gemeinsam zu erstellen, klingt nach einem guten Schritt, damit sich alle gehört fühlen.",
        ],
    },
}

# === Helper: AI response generator ===
import random

def generate_ai_response(language, scenario, user_message):
    # Just pick next AI reply randomly from the pool for now
    responses = AI_RESPONSES[language][scenario]
    return random.choice(responses)

# === Audio to text using SpeechRecognition ===
def audio_to_text(audio_bytes):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(BytesIO(audio_bytes))
    with audio_file as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None

# === Main app ===
def main():
    st.set_page_config(page_title="Teacher-Principal Roleplay Chatbot", layout="wide")

    # Session state initialization
    if "chat_log" not in st.session_state:
        st.session_state.chat_log = []  # List of (speaker, message)

    if "language" not in st.session_state:
        st.session_state.language = "EN"

    if "scenario" not in st.session_state:
        st.session_state.scenario = "Strategic Communication"

    if "input_type" not in st.session_state:
        st.session_state.input_type = "Text Input"

    lang = st.sidebar.selectbox(
        LANG_DATA["EN"]["select_language"], ["EN", "DE"], index=0 if st.session_state.language == "EN" else 1
    )
    st.session_state.language = lang

    scenario_options = {
        "EN": [LANG_DATA["EN"]["scenario_strategic"], LANG_DATA["EN"]["scenario_understanding"]],
        "DE": [LANG_DATA["DE"]["scenario_strategic"], LANG_DATA["DE"]["scenario_understanding"]],
    }
    scenario = st.sidebar.selectbox(
        LANG_DATA[lang]["select_scenario"],
        scenario_options[lang],
        index=0 if st.session_state.scenario == scenario_options[lang][0] else 1,
    )
    st.session_state.scenario = scenario

    input_type = st.sidebar.selectbox(
        LANG_DATA[lang]["select_input"],
        [LANG_DATA[lang]["input_text"], LANG_DATA[lang]["input_audio"]],
        index=0 if st.session_state.input_type == LANG_DATA[lang]["input_text"] else 1,
    )
    st.session_state.input_type = input_type

    # Display teacher instructions
    st.sidebar.markdown(f"### {LANG_DATA[lang]['instructions_title']}")
    st.sidebar.info(LANG_DATA[lang]["instructions_teacher"])
    st.sidebar.markdown(f"**{LANG_DATA[lang]['scenario_desc'][scenario]}**")

    st.title(LANG_DATA[lang]["title"])

    # Conversation display
    st.markdown(f"## {LANG_DATA[lang]['conversation_log']}")
    for speaker, msg in st.session_state.chat_log:
        if speaker == "teacher":
            st.markdown(f"**{LANG_DATA[lang]['role_teacher']}** {msg}")
        else:
            st.markdown(f"**{LANG_DATA[lang]['role_principal']}** {msg}")

    # Input area
    user_input = None

    if input_type == LANG_DATA[lang]["input_text"]:
        user_input = st.text_input(LANG_DATA[lang]["type_message"], key="user_text_input")
        submit = st.button(LANG_DATA[lang]["send"])
        if submit and user_input:
            # Log teacher input
            st.session_state.chat_log.append(("teacher", user_input))
            # Generate AI response aligned with scenario
            ai_resp = generate_ai_response(lang, scenario, user_input)
            st.session_state.chat_log.append(("principal", ai_resp))
            # Clear input box
            st.session_state.user_text_input = ""

    elif input_type == LANG_DATA[lang]["input_audio"]:
        st.write(LANG_DATA[lang]["record_audio"])
        audio_bytes = st.file_uploader("Upload a WAV audio file (max 10MB)", type=["wav"], key="audio_uploader")

        if audio_bytes is not None:
            with st.spinner(LANG_DATA[lang]["listening"]):
                recognized_text = audio_to_text(audio_bytes.read())
            if recognized_text:
                st.markdown(f"> **You said:** {recognized_text}")
                # Log teacher input
                st.session_state.chat_log.append(("teacher", recognized_text))
                # Generate AI response aligned with scenario
                ai_resp = generate_ai_response(lang, scenario, recognized_text)
                st.session_state.chat_log.append(("principal", ai_resp))
            else:
                st.error(LANG_DATA[lang]["error_audio"])

    # Add a "Clear Chat" button
    if st.button("Clear Conversation"):
        st.session_state.chat_log = []

if __name__ == "__main__":
    main()
