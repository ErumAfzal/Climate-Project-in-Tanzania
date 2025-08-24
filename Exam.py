# roleplay_chat_simulation.py
# Streamlit app for humanized, multi-turn role-play conversations (10 scenarios)
# Author: OpenAI GPT-5 Mini
# Usage: streamlit run roleplay_chat_simulation.py

import streamlit as st

# ---------------------------
# Helper functions
# ---------------------------

def initialize_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""
    if 'current_scenario' not in st.session_state:
        st.session_state.current_scenario = None

def add_message(role, message):
    st.session_state.chat_history.append({"role": role, "message": message})

def get_roleplay_prompt(scenario_id):
    """
    Returns initial system message or AI prompt for each scenario.
    Humanized, English version.
    """
    roleplay_prompts = {
        1: "You are a teacher discussing a student's math grade with a concerned parent. Respond kindly, clearly, and humanly, explaining the reasoning and listening carefully.",
        2: "You are a teacher moderating a class discussion about a study trip. Respond thoughtfully, listen to students, and guide the discussion democratically.",
        3: "You are a career advisor talking with a student about their post-graduation plans. Provide supportive guidance, ask clarifying questions, and help explore options.",
        4: "You are a teacher discussing a new feedback culture with your principal. Be professional, give your opinions carefully, and suggest constructive changes.",
        5: "You are collaborating with a colleague to develop a parent interview guide. Be cooperative, suggest relevant aspects, and consider the colleague's perspective.",
        6: "You are discussing self-directed learning training with your supervisor. Humanize your responses, express hesitations and clarifications naturally, and connect it to school goals.",
        7: "You are a student explaining why you want to go to a particular historical site for a study trip. Make your arguments politely, but firmly, and listen to the teacher's advice.",
        8: "You are a student discussing career choices with a teacher. Express creative ambitions and realistic concerns, asking for guidance without being forced.",
        9: "You are a teacher sharing skepticism about a new evaluation culture with your principal. Be clear, constructive, and suggest ways to improve the process.",
        10: "You are a teacher brainstorming a parent interview guide with a colleague. Suggest ideas, give examples, and respond respectfully to counterpoints."
    }
    return roleplay_prompts.get(scenario_id, "You are a participant in a professional role-play scenario. Respond politely and clearly.")

def generate_ai_response(user_input, scenario_id):
    """
    Humanized AI response logic.
    For demonstration, uses simple scripted/humanized style.
    In production, could integrate GPT API for dynamic responses.
    """
    base_prompt = get_roleplay_prompt(scenario_id)
    
    # Simple humanized behavior: hesitations, clarifications, friendly tone
    if "?" in user_input:
        response = f"Hmm, that's a good question. Let me think... Well, regarding that, {user_input.lower()} I believe we could approach it this way."
    elif any(word in user_input.lower() for word in ["concerned", "worried", "problem", "issue"]):
        response = f"I understand your concern. Honestly, it can be challenging, but let's look at it step by step."
    elif len(user_input.strip()) == 0:
        response = "Could you please clarify what you mean?"
    else:
        response = f"Ah, I see. So you're saying: '{user_input}'. That makes sense. Let's discuss this a bit further."
    
    # Add slight human hesitation
    response = "Hmm... " + response
    return response

# ---------------------------
# Streamlit App
# ---------------------------

st.set_page_config(page_title="Role-Play Chat Simulation", layout="wide")

st.title("Professional Role-Play Chat Simulation")
st.markdown("""
Welcome! Select one of the 10 role-play scenarios below and engage in a humanized, multi-turn conversation.
The AI will respond with natural pauses, clarifications, and friendly tone.
""")

initialize_session_state()

# Scenario selection
scenario_options = [
    "1: Student Math Grade Discussion",
    "2: Class Study Trip Moderation",
    "3: Career Counseling Session",
    "4: Feedback Culture Discussion with Principal",
    "5: Parent Interview Guide Development",
    "6: Self-Directed Learning Training Discussion",
    "7: Student Study Trip Proposal",
    "8: Career Choices Consultation",
    "9: Evaluation Culture Skepticism",
    "10: Brainstorm Parent Interview Guide"
]

selected_scenario = st.selectbox("Select Role-Play Scenario", scenario_options)

if selected_scenario != st.session_state.current_scenario:
    # Reset chat for new scenario
    st.session_state.chat_history = []
    st.session_state.user_input = ""
    st.session_state.current_scenario = selected_scenario
    add_message("AI", f"Hello! Welcome to scenario '{selected_scenario}'. Let's start our conversation. How would you like to begin?")

# Chat history display
st.subheader("Conversation")
chat_container = st.container()
with chat_container:
    for chat in st.session_state.chat_history:
        if chat["role"] == "AI":
            st.markdown(f"**AI:** {chat['message']}")
        else:
            st.markdown(f"**You:** {chat['message']}")

# User input
st.subheader("Your Input")
user_input = st.text_input("Type your message here...", key="user_input")

if st.button("Send") and user_input.strip() != "":
    # Add user message
    add_message("User", user_input)
    
    # Generate AI response
    ai_reply = generate_ai_response(user_input, int(st.session_state.current_scenario.split(":")[0]))
    add_message("AI", ai_reply)
    
    # Clear input box
    st.session_state.user_input = ""
    
    # Scroll to bottom (workaround)
    st.experimental_rerun()
