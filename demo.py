import streamlit as st
import openai
import time
import os
import json
from gtts import gTTS

# --- Configuration ---
st.set_page_config(page_title="Multi-Agent Role-Play Simulator", layout="centered")
st.title("Role-Play Simulator Based on Communicative Action Theory")

# --- Language Selection ---
language = st.sidebar.selectbox("Language / Sprache", ["English", "Deutsch"])

# --- API Key Input ---
api_key = st.text_input("Enter your OpenAI API key:", type="password")
if not api_key:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()
openai.api_key = api_key

# --- Role-Play Scenarios Dictionary (Placeholders: add full text as needed) ---
SCENARIOS = {
    "Role Play 1 – Self-Directed Learning": {
        "instructions_en": "You are a teacher requesting approval to attend a self-directed learning workshop. Your goal is to convince the principal.",
        "instructions_de": "Sie sind eine Lehrkraft, die die Genehmigung für eine Fortbildung zum selbstgesteuerten Lernen beantragt.",
        "system_prompt_en": "You are the principal who is skeptical about self-directed learning. Ask critical questions and demand justification.",
        "system_prompt_de": "Sie sind die Schulleitung und skeptisch gegenüber selbstgesteuertem Lernen. Stellen Sie kritische Fragen und verlangen Sie Rechtfertigungen.",
        "type": "Strategic",
        "social_role": {"user": "Weak", "assistant": "Strong"}
    },
    "Role Play 2 – Feedback Culture Introduction": {
        "instructions_en": "You are a teacher trying to initiate a feedback culture in the department. The colleague may resist the idea.",
        "instructions_de": "Sie möchten in Ihrer Abteilung eine Feedbackkultur einführen. Ihr/e Kolleg/in ist skeptisch.",
        "system_prompt_en": "You are a skeptical colleague. Ask whether the feedback process is practical and valuable.",
        "system_prompt_de": "Sie sind skeptisch gegenüber Feedbackkultur. Stellen Sie Fragen zur Umsetzbarkeit und zum Nutzen.",
        "type": "Understanding-Oriented",
        "social_role": {"user": "Equal", "assistant": "Equal"}
    },
    # Add Role Play 3-10 here...
}

# --- Sidebar Selection ---
scenario_name = st.sidebar.selectbox("Choose Role Play", list(SCENARIOS.keys()))
scenario = SCENARIOS[scenario_name]

# --- Load Scenario Instructions ---
if language == "English":
    instructions = scenario["instructions_en"]
    system_prompt = scenario["system_prompt_en"]
    lang_code = "en"
else:
    instructions = scenario["instructions_de"]
    system_prompt = scenario["system_prompt_de"]
    lang_code = "de"

# --- Display Instructions ---
st.subheader("Instructions")
st.markdown(instructions)

# --- Start Role Play ---
if st.button("Start Role-Play"):
    st.session_state.chat_ready = True
    st.session_state.conversation = [{"role": "system", "content": system_prompt}]
    st.session_state.chat_log = []

# --- Chat Loop ---
if st.session_state.get("chat_ready", False):
    user_input = st.text_input("You:", key="user_input")
    if st.button("Send") and user_input.strip():
        st.session_state.conversation.append({"role": "user", "content": user_input})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=st.session_state.conversation,
                temperature=0.7,
                max_tokens=512,
            )
            assistant_reply = response.choices[0].message["content"].strip()
        except Exception as e:
            assistant_reply = f"⚠️ Error: {str(e)}"

        st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})
        st.session_state.chat_log.append({
            "user": user_input,
            "assistant": assistant_reply,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })

# --- Display Chat ---
if st.session_state.get("conversation"):
    st.subheader("Dialogue")
    for msg in st.session_state.conversation[1:]:  # Skip system
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**Partner:** {msg['content']}")

# --- Save Chat Log ---
if st.button("Save Chat Log"):
    filename = f"chatlog_{scenario_name.replace(' ', '_')}_{time.time_ns()}.json"
    os.makedirs("logs", exist_ok=True)
    with open(f"logs/{filename}", "w", encoding="utf-8") as f:
        json.dump(st.session_state.chat_log, f, indent=2, ensure_ascii=False)
    st.success(f"Chat log saved as {filename}")
