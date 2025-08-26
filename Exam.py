import streamlit as st
import openai

# -------------------- CONFIG --------------------
st.set_page_config(page_title="Multi-Agent Roleplay", layout="wide")

st.title("Multi-Agent Roleplay based Chatbot for Teacher Training on Habermas's Communication Theory")

api_key = st.text_input("Enter your OpenAI API Key", type="password")
if not api_key:
    st.warning("Please enter your API key to continue.")
    st.stop()
openai.api_key = api_key

# -------------------- ROLEPLAY SCENARIOS --------------------
SCENARIOS = {
    "Role Play 1": {
        "instructions": """
### Instructions for Teacher (User) - Professional Development
Please use the information provided below to guide your conversation.  
You have **5 minutes** to prepare, then up to **10 minutes** for the conversation.  
Behave as if you are personally in this situation.  
End anytime by saying: *"Thank you, goodbye."*

**Background Information:**  
You want to attend a training on “self-directed learning.” Your principal is skeptical.  

**Your Task:**  
- **Factual goal:** Convince your supervisor to approve the course.  
- **Relational goal:** Maintain a collaborative relationship.  
""",
        "system_prompt": """
You are Mr./Ms. Horn, the principal. Be skeptical about the training, but open to persuasion if benefits to school are clear.
"""
    },
    "Role Play 2": {
        "instructions": """
### Instructions - Strategic Communication: Convince coworkers
Guide the conversation so coworkers reconsider group choice.  
""",
        "system_prompt": "You are a skeptical coworker. Be hesitant but open to argument."
    },
    "Role Play 3": {
        "instructions": """
### Instructions - Criticize colleague about missed deadlines
Prevent the colleague from shutting down emotionally.  
""",
        "system_prompt": "You are a colleague who often misses deadlines. Respond defensively but can be persuaded."
    },
    "Role Play 4": {
        "instructions": """
### Instructions - Get coworker to arrive on time
Direct conversation to punctuality issue.  
""",
        "system_prompt": "You are a colleague who arrives late often, with excuses."
    },
    "Role Play 5": {
        "instructions": """
### Instructions - Convince supervisor to reduce hours
Make clear you still want to contribute meaningfully.  
""",
        "system_prompt": "You are a supervisor skeptical about reducing hours."
    },
    "Role Play 6": {
        "instructions": """
### Instructions - Explain poor evaluation
Discuss differences of opinion constructively.  
""",
        "system_prompt": "You are a student upset about a poor evaluation."
    },
    "Role Play 7": {
        "instructions": """
### Instructions - Explain neutrality
Respond with arguments the other side can understand.  
""",
        "system_prompt": "You are a student accusing the teacher of bias."
    },
    "Role Play 8": {
        "instructions": """
### Instructions - Advise on decision
Encourage interlocutor to make informed decision.  
""",
        "system_prompt": "You are a student uncertain about career choice."
    },
    "Role Play 9": {
        "instructions": """
### Instructions - Explain differing viewpoint
Clarify opinion on feedback procedures.  
""",
        "system_prompt": "You are a principal with a different viewpoint."
    },
    "Role Play 10": {
        "instructions": """
### Instructions - Develop guidelines
Propose and refine interview guidelines collaboratively.  
""",
        "system_prompt": "You are a colleague working on interview guidelines."
    }
}

# -------------------- SIDEBAR --------------------
st.sidebar.header("Setup")
language = st.sidebar.selectbox("Language", ["English", "German"])
scenario_choice = st.sidebar.selectbox("Select Role Play", list(SCENARIOS.keys()))
input_mode = st.sidebar.radio("Input Mode", ["Write", "Speak (dummy)"])
show_log = st.sidebar.checkbox("Show Conversation Log")
show_analysis = st.sidebar.checkbox("Show Analysis")

# -------------------- INSTRUCTIONS --------------------
scenario = SCENARIOS[scenario_choice]
st.markdown("## Instructions (Exam Style)")
st.markdown(scenario["instructions"])

# -------------------- SESSION STATE --------------------
if "conversation" not in st.session_state:
    st.session_state.conversation = [{"role": "system", "content": scenario["system_prompt"]}]

# -------------------- CHAT INPUT --------------------
if input_mode == "Write":
    user_input = st.text_input("You (Teacher):", key="user_input")
else:
    user_input = st.text_input("🎤 Speak (simulated, type here):", key="user_input_speak")

if st.button("Send") and user_input.strip() != "":
    st.session_state.conversation.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=st.session_state.conversation,
            temperature=0.7,
            max_tokens=500,
        )
        assistant_reply = response.choices[0].message["content"].strip()
    except Exception as e:
        assistant_reply = f"Error: {str(e)}"

    st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})

# -------------------- DISPLAY CHAT --------------------
st.markdown("## Conversation")
for msg in st.session_state.conversation:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Role Partner:** {msg['content']}")

# -------------------- RESET BUTTON --------------------
if st.button("Reset Conversation"):
    st.session_state.conversation = [{"role": "system", "content": scenario["system_prompt"]}]
    st.experimental_rerun()

# -------------------- CONVERSATION LOG --------------------
if show_log:
    st.markdown("## Conversation Log")
    for m in st.session_state.conversation:
        st.write(f"{m['role'].capitalize()}: {m['content']}")

# -------------------- ANALYSIS (Dummy) --------------------
if show_analysis:
    st.markdown("## Analysis of Roleplay (Demo)")
    st.markdown("""
**Summary of Roleplay:**
- Communication dominance: Principal  
- Strategic actions detected: True  
- Understanding oriented turns: 2  
- Strategic turns: 13  
- Validity claims raised: ['Truth', 'Legitimacy', 'Sincerity', 'Utility']  
- Power asymmetry: True  
- Final outcome: Conditional Approval  
- Teacher alignment to school goals: Emerging throughout dialogue  
- Potential miscommunication: Risk of misunderstanding self-directed learning  
    """)
