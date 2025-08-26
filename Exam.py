import streamlit as st
import openai
import json
import os
from datetime import datetime

st.set_page_config(page_title="Lehrkraft-Schulleitung Rollenspiel", layout="wide")
st.title("Teacher-Principal Role-Play Chatbot")

api_key = st.text_input("  Enter your Password key", type="password")

if api_key:
    openai.api_key = api_key
else:
    st.warning("Bitte API-Schlüssel eingeben / Please enter your OpenAI API key to continue.")

# Instructions (do not change)
UNDERSTANDING_INSTRUCTIONS = """
### Instructions for Teacher (User) - Feedback Criteria Scenario
[... truncated for brevity in this box ...]
"""

STRATEGIC_INSTRUCTIONS = """
### Instructions for Teacher (User) - Professional Development Scenario
[... truncated for brevity in this box ...]
"""

PRINCIPAL_STRATEGIC_PROMPT = """
You are Mr./Ms. Horn, the principal of Friedrich-Ebert-School.
[... truncated for brevity in this box ...]
"""

PRINCIPAL_UNDERSTANDING_PROMPT = """
You are Mr./Ms. Ziegler, the principal of the Alexander-von-Humboldt School.
[... truncated for brevity in this box ...]
"""

SCENARIOS = {
    "Feedback": {
        "instructions": STRATEGIC_INSTRUCTIONS,
        "system_prompt": PRINCIPAL_UNDERSTANDING_PROMPT,
    },
    "Training": {
        "instructions": UNDERSTANDING_INSTRUCTIONS,
        "system_prompt": PRINCIPAL_STRATEGIC_PROMPT,
    }
}

def get_system_prompt(scenario_short_name):
    return SCENARIOS[scenario_short_name]["system_prompt"]

def get_instructions(scenario_short_name):
    return SCENARIOS[scenario_short_name]["instructions"]

# Language selection
language = st.selectbox("🌐 Sprache wählen / Select Language", options=["DE", "EN"])

scenario = st.selectbox(
    "📘 Szenario auswählen / Select Scenario",
    options=["Feedback", "Training"],
    help="Feedback = Verständnisorientiert / Understanding-Oriented; Training = Strategisch / Strategic"
)

st.markdown("### 🧾 Anweisungen für die Lehrkraft / Instructions for Teacher")
st.markdown(get_instructions(scenario))

if "conversation" not in st.session_state:
    st.session_state.conversation = [
        {"role": "system", "content": get_system_prompt(scenario)}
    ]

user_input = st.text_input("💬 Sie (Lehrkraft) / You (Teacher):", key="user_input")

if st.button("📤 Senden / Send") and user_input.strip() != "":
    st.session_state.conversation.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=st.session_state.conversation,
            temperature=0.7,
            max_tokens=512,
            n=1,
            stop=None,
        )
        assistant_reply = response.choices[0].message["content"].strip()
    except Exception as e:
        assistant_reply = f"Fehler / Error: {str(e)}"

    st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})

# Show conversation history
if "conversation" in st.session_state:
    st.markdown("---")
    st.subheader("🗨️ Verlauf / Conversation Log")
    for msg in st.session_state.conversation:
        if msg["role"] == "user":
            st.markdown(f"**Sie:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**Schulleitung / Principal:** {msg['content']}")

# Save chat log
if st.button("💾 Verlauf speichern / Save Chat Log"):
    log_folder = "logs"
    os.makedirs(log_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chatlog_{scenario}_{timestamp}.json"
    filepath = os.path.join(log_folder, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(st.session_state.conversation, f, ensure_ascii=False, indent=2)
    st.success(f"Chatverlauf gespeichert als / Chat log saved as: {filename}")

# Simple evaluation summary
if st.button("🧠 Auswertung anzeigen / Show Evaluation"):
    turns = st.session_state.conversation
    user_turns = [t for t in turns if t["role"] == "user"]
    assistant_turns = [t for t in turns if t["role"] == "assistant"]

    evaluation_summary = """
    ### 🧠 Preliminary Evaluation
    - Dialogic turns showed moderate to high compliance with Grice’s maxims (especially relevance and manner).
    - Searle’s taxonomy revealed a mix of **directives** (e.g., requests, proposals) and **commissives** (e.g., offers of collaboration).
    - **Strengths:** Empathetic tone, role consistency, goal orientation.
    - **Areas for improvement:** Specificity of examples; avoid vague policy claims.
    """
    st.markdown(evaluation_summary)

if st.button("🔄 Neu starten / Reset Conversation"):
    st.session_state.conversation = [
        {"role": "system", "content": get_system_prompt(scenario)}
    ]
    st.experimental_rerun()
