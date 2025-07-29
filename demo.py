import streamlit as st
import openai
import time
import os
import json

# --- App Configuration ---
st.set_page_config(page_title="Habermas Role-Play Chatbot", layout="centered")
st.title("🎭 Communicative Action Role-Play Simulator")

# --- API Key Input ---
api_key = st.text_input("🔑 Enter your OpenAI API key:", type="password")
if not api_key:
    st.warning("Please enter your key to continue.")
    st.stop()
openai.api_key = api_key

# --- Role-Play Scenarios (expandable) ---
SCENARIOS = {
    "Training (Strategic Communication)": {
        "instructions_en": """
        ### Instructions for Teacher (User)
        [English instructions here, same as before...]
        """,
        "instructions_de": """
        ### Anweisungen für Lehrkraft (Benutzer)
        [German version of the same scenario...]
        """,
        "system_prompt": """[Principal's prompt as you had it]""",
        "type": "Strategic"
    },
    # Add more scenarios like: "Collaboration", "Disciplinary Talk", etc.
}

# --- Sidebar Inputs ---
st.sidebar.header("🧭 Scenario Configuration")
language = st.sidebar.selectbox("🌐 Language", ["English", "Deutsch"])
scenario = st.sidebar.selectbox("🎯 Select Role-Play", list(SCENARIOS.keys()))

# --- Instruction & Prompt Setup ---
instructions = SCENARIOS[scenario]["instructions_en"] if language == "English" else SCENARIOS[scenario]["instructions_de"]
system_prompt = SCENARIOS[scenario]["system_prompt"]

# --- Timer Logic ---
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
    st.session_state.timer_started = False
    st.session_state.chat_ready = False
    st.session_state.conversation = [{"role": "system", "content": system_prompt}]
    st.session_state.chat_log = []

# --- Show Instructions + Countdown ---
st.markdown("### 📝 Instructions")
st.markdown(instructions)

if not st.session_state.timer_started:
    if st.button("✅ I have read the instructions. Start countdown."):
        st.session_state.start_time = time.time()
        st.session_state.timer_started = True

if st.session_state.timer_started and not st.session_state.chat_ready:
    elapsed = time.time() - st.session_state.start_time
    remaining = int(120 - elapsed)
    if remaining > 0:
        st.info(f"⏳ Chat will start in {remaining} seconds.")
        st.stop()
    else:
        st.session_state.chat_ready = True
        st.success("✅ You may now begin your conversation.")

# --- Chat Interface ---
if st.session_state.chat_ready:
    user_input = st.text_input("You (Teacher):", key="user_input")

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

# --- Chat Display ---
if "conversation" in st.session_state:
    st.markdown("### 💬 Dialogue")
    for msg in st.session_state.conversation[1:]:  # skip system
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**Principal:** {msg['content']}")

# --- Reset and Save ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🔁 Reset Conversation"):
        st.session_state.conversation = [{"role": "system", "content": system_prompt}]
        st.session_state.chat_log = []
        st.experimental_rerun()

with col2:
    if st.button("💾 Save Chat Log"):
        filename = f"chatlog_{scenario.replace(' ', '_')}_{time.time_ns()}.json"
        os.makedirs("logs", exist_ok=True)
        with open(f"logs/{filename}", "w", encoding="utf-8") as f:
            json.dump(st.session_state.chat_log, f, indent=2, ensure_ascii=False)
        st.success(f"Chat log saved as {filename}")

# (Optional) Post-analysis placeholder
if st.button("📊 Analyze Conversation"):
    st.info("This is a placeholder. In final version, we will show Grice/Searle evaluation here.")
    # To be implemented later using regex, dialogue acts, etc.
