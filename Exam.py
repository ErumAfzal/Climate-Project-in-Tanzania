import streamlit as st
import random
import time

# --- Initialize session state safely ---
if "messages" not in st.session_state:
    st.session_state.messages = []  # stores chat history

if "user_input" not in st.session_state:
    st.session_state.user_input = ""  # stores current input

if "role_play" not in st.session_state:
    st.session_state.role_play = "Select a Role Play"

# --- Define role-play data ---
ROLE_PLAYS = {
    "Role Play 1": {
        "description": "You are a teacher at Astrid-Lindgren-School discussing team coordination...",
        "persona": "Teacher addressing a colleague about deadlines, trying to remain constructive.",
        "instructions": """
1. Stay professional but constructive.
2. Explain your viewpoint clearly.
3. Listen actively to the colleague.
4. Goal: Improve team coordination without conflict.
"""
    },
    "Role Play 2": {
        "description": "You are Mr/Ms Krause, a teacher confident about time management...",
        "persona": "Respond constructively while remaining relaxed, using standard phrases.",
        "instructions": """
1. Maintain relaxed and confident demeanor.
2. Support colleagues if needed.
3. Goal: Resolve timing conflicts without stress.
"""
    },
    "Role Play 3": {
        "description": "You are a trainee teacher handling a chronically late student...",
        "persona": "Directly address the student, explain consequences, remain firm.",
        "instructions": """
1. Address the lateness issue calmly but firmly.
2. Explain classroom rules and consequences.
3. Goal: Encourage punctuality.
"""
    },
    "Role Play 4": {
        "description": "You are a student who frequently comes late, with excuses...",
        "persona": "Minimize immediate consequences, try to negotiate, remain polite.",
        "instructions": """
1. Give excuses politely and reasonably.
2. Try to negotiate consequences.
3. Goal: Avoid major penalties.
"""
    },
    "Role Play 5": {
        "description": "Requesting a reduction of working hours from your principal...",
        "persona": "Explain personal motivations, maintain good relationship, handle objections.",
        "instructions": """
1. Be clear about your reasons.
2. Remain professional and respectful.
3. Goal: Achieve working hour reduction without conflict.
"""
    },
    "Role Play 6": {
        "description": "Parent-teacher conversation about student's math grade...",
        "persona": "Justify the grade while remaining open to discussion and empathetic.",
        "instructions": """
1. Present the grade rationale clearly.
2. Listen to parent's concerns.
3. Goal: Maintain fairness while fostering understanding.
"""
    },
    "Role Play 7": {
        "description": "Moderating a student discussion about class field trip destination...",
        "persona": "Encourage fair discussion, ensure all voices are heard, explain moderation role.",
        "instructions": """
1. Facilitate equitable discussion.
2. Explain your role as moderator.
3. Goal: Reach a consensus acceptable to most students.
"""
    },
    "Role Play 8": {
        "description": "Career counseling session with a student considering creative vs secure paths...",
        "persona": "Listen, guide, provide structured advice without imposing personal opinion.",
        "instructions": """
1. Ask guiding questions.
2. Offer structured but neutral advice.
3. Goal: Help student clarify career options.
"""
    },
    "Role Play 9": {
        "description": "Teacher discussing feedback culture with principal...",
        "persona": "Present perspective, suggest improvements, maintain respectful dialogue.",
        "instructions": """
1. Present your suggestions clearly.
2. Maintain respect for authority.
3. Goal: Influence feedback criteria positively while cooperating.
"""
    },
    "Role Play 10": {
        "description": "Collaborating on an parents' interview guideline to gather student-related insights...",
        "persona": "Generate aspects for discussion, validate partner’s points, maintain cooperative tone.",
        "instructions": """
1. Brainstorm relevant aspects collaboratively.
2. Validate colleagues’ points.
3. Goal: Generate comprehensive and practical guidelines.
"""
    },
}

# --- Streamlit UI ---
st.set_page_config(page_title="Role Play Simulator", layout="wide")
st.title("Interactive Role Play Simulator")
st.markdown("""
This platform allows you to simulate and practice professional role-play scenarios.
Select a role play from the sidebar and interact as you would in a real conversation.
""")

# --- Sidebar for role play selection ---
st.sidebar.header("Select Role Play")
st.session_state.role_play = st.sidebar.selectbox(
    "Role Play Scenario",
    options=list(ROLE_PLAYS.keys())
)

# --- Show description, persona, and instructions ---
role_info = ROLE_PLAYS[st.session_state.role_play]

st.subheader(f"{st.session_state.role_play}")
st.markdown(f"**Scenario:** {role_info['description']}")
st.markdown(f"**Persona Guidance:** {role_info['persona']}")

st.expander("View Role Play Instructions", expanded=True).markdown(role_info['instructions'])

# --- Chat interface ---
st.subheader("Conversation")
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Simulator:** {message['content']}")

# --- Humanized AI response generator ---
def generate_humanized_response(user_text):
    hesitations = ["Hmm,", "Well,", "I see,", "Right,", "Ah,"]
    filler = ["let me think...", "that's interesting.", "okay.", "I understand."]
    time.sleep(0.5)  # simulate thinking
    return f"{random.choice(hesitations)} {random.choice(filler)} About what you said: '{user_text}', how would you like to proceed?"

# --- Handle user input ---
def handle_user_input():
    user_text = st.session_state.user_input.strip()
    if user_text:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_text})

        # Generate AI response
        ai_response = generate_humanized_response(user_text)
        st.session_state.messages.append({"role": "ai", "content": ai_response})

        # Clear input safely
        st.session_state.user_input = ""

st.text_input(
    "Your input:",
    key="user_input",
    on_change=handle_user_input
)

# --- Reset chat button ---
if st.button("Reset Chat"):
    st.session_state.messages = []
    st.session_state.user_input = ""
