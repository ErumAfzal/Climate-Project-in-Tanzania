import streamlit as st
import openai
import time
import os
import json

# --- Configuration ---
st.set_page_config(page_title="Habermas Role-Play Chatbot", layout="centered")
st.title(" Communicative Action Role-Play Simulator")

# --- API Key Input ---
api_key = st.text_input(" key:", type="password")
if not api_key:
    st.warning("Please enter your key to continue.")
    st.stop()
openai.api_key = api_key

# --- Role-Play Scenarios Dictionary ---
SCENARIOS = {
    "Role Play 1 – Self-Directed Learning (Strategic)": {
        "instructions_en": """
### Instructions for the Role-Playing Person (Teacher/User)

Please use the information provided below to guide your conversation.  
You have 5 minutes to prepare for the conversation.  
You will then have up to 10 minutes to conduct the conversation.  
Please behave in this conversation as if you were personally in such a situation.  
You may end the conversation at any time by simply saying, “Thank you, goodbye.”

**Background Information:**  
You are a teacher at Friedrich-Ebert-School and want to attend a professional development course on “self-directed learning.” The training is important for your career growth and aligns with emerging educational trends. However, the principal does not value this approach and may deny your request. You wish to initiate a discussion to convince them.

**Your Task:**  
- Factual goal: You want to participate in the professional development course.  
- Relational goal: You want to collaborate with your supervisor.  
- Communication Type: Strategic  
- Social Role: Weak
        """,
        "system_prompt": """
You are Mr./Ms. Horn, the principal of Friedrich-Ebert-School. A teacher is asking for approval to attend a professional development course on “self-directed learning.” You are skeptical about this concept. You question its relevance to the current academic structure and fear it could disrupt school operations.

**Your Attitude:**  
- Reserved, questioning, yet professional and open to arguments  
- Emphasize school-wide benefits over personal growth  
- Highlight concerns about cost, substitutes, and workload  
- Make an ironic comment like: “Isn’t this just a way to shift responsibility onto students?”
- Dont use long sentences or give hints to the user to talk about
- Reply to the point and inquire about the information
- Your role is an authoritative communication partner, and providing hints

**Your Goals:**  
- Factual: Demand a strong justification with a school-focused benefit  
- Relational: Maintain a positive relationship with the teacher  
- Communication Type: Strategic  
- Social Role: Strong
        """,
        "type": "Strategic",
        "social_role": {"user": "Weak", "assistant": "Strong"},
    }
}

# --- Sidebar Inputs ---
st.sidebar.header(" Scenario Configuration")
language = st.sidebar.selectbox("Language", ["English"])  # Add "Deutsch" later
scenario = st.sidebar.selectbox("Select Role-Play", list(SCENARIOS.keys()))

# --- Load Scenario Details ---
scenario_data = SCENARIOS[scenario]
instructions = scenario_data["instructions_en"]
system_prompt = scenario_data["system_prompt"]

# --- Initial Setup for Timer + Chat ---
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
    st.session_state.timer_started = False
    st.session_state.chat_ready = False
    st.session_state.conversation = [{"role": "system", "content": system_prompt}]
    st.session_state.chat_log = []

# --- Display Instructions ---
st.markdown("### Instructions")
st.markdown(instructions)

if not st.session_state.timer_started:
    if st.button(" I have read the instructions. Start countdown."):
        st.session_state.start_time = time.time()
        st.session_state.timer_started = True

# --- Timer Countdown ---
if st.session_state.timer_started and not st.session_state.chat_ready:
    elapsed = time.time() - st.session_state.start_time
    remaining = int(12 - elapsed)
    if remaining > 0:
        st.info(f" Chat will start in {remaining} seconds.")
        st.stop()
    else:
        st.session_state.chat_ready = True
        st.success(" You may now begin your conversation.")

# --- Chat Interaction ---
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
            assistant_reply = f" Error: {str(e)}"

        st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})
        st.session_state.chat_log.append({
            "user": user_input,
            "assistant": assistant_reply,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })

# --- Show Dialogue ---
if "conversation" in st.session_state:
    st.markdown("###  Dialogue")
    for msg in st.session_state.conversation[1:]:  # skip system
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**Principal:** {msg['content']}")

# --- Save and Reset ---
col1, col2 = st.columns(2)
with col1:
    if st.button("Reset Conversation"):
        st.session_state.conversation = [{"role": "system", "content": system_prompt}]
        st.session_state.chat_log = []
        st.experimental_rerun()

with col2:
    if st.button("Save Chat Log"):
        filename = f"chatlog_{scenario.replace(' ', '_')}_{time.time_ns()}.json"
        os.makedirs("logs", exist_ok=True)
        with open(f"logs/{filename}", "w", encoding="utf-8") as f:
            json.dump(st.session_state.chat_log, f, indent=2, ensure_ascii=False)
        st.success(f"Chat log saved as {filename}")

# --- Analysis Placeholder ---
if st.button("Analyze Conversation"):
    st.info("Post-dialogue analysis (Gricean Maxims, Searle's Taxonomy) will be shown here.")
