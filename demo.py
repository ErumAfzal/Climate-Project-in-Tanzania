import streamlit as st
import time
import openai
from datetime import datetime

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "your-api-key"

# Title
st.title("Multi-Agent Role-Play Chatbot (Habermas-Inspired)")

# Define your roleplay scenarios
SCENARIOS = {
    "Role Play 1 – Classroom Management (Strategic)": {
        "instructions_en": """
### Instructions for the Role-Playing Person (Teacher/User)

You are a teacher at a secondary school. You have noticed that a student regularly disrupts your lessons, affecting the learning environment for others. You are seeking support from the school principal.  

- **Factual Goal**: Request support and intervention to address the disruptive student.  
- **Relational Goal**: Maintain authority and express that the issue needs administrative attention.  
- **Communication Type**: Strategic  
- **Social Role**: Subordinate (teacher) to superior (principal)

You may end the conversation at any time by saying, “Thank you, goodbye.”
""",
        "system_prompt": """
You are the school principal. A teacher has approached you with concerns about a student's repeated misbehavior.

Your task is to manage the conversation in a professional manner, listen actively, and maintain school policies while balancing the teacher's needs.  

**Principal's Goals**:  
- **Factual**: Gather facts about the behavior.  
- **Strategic**: Avoid making hasty decisions.  
- **Relational**: Show leadership but remain open.

**Respond appropriately** using strategic communication. Use directive and commissive speech acts.  
End the conversation by proposing a follow-up action (e.g., observation or parent meeting).
""",
        "type": "Strategic",
        "social_role": {"user": "Subordinate", "assistant": "Superior"},
    },

    "Role Play 2 – Feedback Culture Introduction (Understanding-Oriented)": {
        "instructions_en": """
### Instructions for the Role-Playing Person (Teacher/User)

You are a teacher at the Alexander-von-Humboldt School. The school leadership is implementing a feedback culture, including peer observations and student feedback.

You believe teacher self-reflection and informal input from colleagues already ensure quality.  
You are skeptical of the current criteria, which focus too much on teacher personality instead of contextual factors (e.g., class size, tools, time constraints).  

- **Factual Goal**: Share your perspective and request a reformulation of the feedback criteria.  
- **Relational Goal**: Maintain a positive professional relationship with the principal.  
- **Communication Type**: Understanding-Oriented  
- **Social Role**: Equal

You may end the conversation at any time by saying, “Thank you, goodbye.”
""",
        "system_prompt": """
You are Ms. Ziegler, the principal of Alexander-von-Humboldt School.  
A teacher wants to talk to you about concerns with the newly introduced feedback culture initiative.

**Your Context:**  
- You believe external perspectives (peer and student feedback) are essential for improving teaching.
- This is not about control, but collegial development and school-wide learning.
- The feedback criteria draft exists but is open for revision.

**Your Goals:**  
- **Factual**: Defend the feedback initiative while staying open to input on criteria.  
- **Relational**: Supportive, professional, and open-minded.

**Your Behavior Guidelines:**  
- Be encouraging and welcoming.  
- Emphasize the collective nature of this initiative.  
- Acknowledge discomfort but reaffirm the purpose: development, not discipline.  
- Accept arguments only if they:
  1. Demonstrate understanding of your goals  
  2. Are clearly stated  
  3. Contain concrete suggestions  
- Suggest organizing a meeting with colleagues to refine the criteria together.  
- End the conversation with a follow-up action (e.g., send email or Doodle for a meeting).
""",
        "type": "Understanding-Oriented",
        "social_role": {"user": "Equal", "assistant": "Equal"},
    },
}

# Select scenario and language
scenario_key = st.selectbox("Select a Role-Play Scenario", list(SCENARIOS.keys()))
language = st.radio("Choose Language", ["English"])  # Expandable in the future
scenario = SCENARIOS[scenario_key]

# Show instructions
st.subheader("Instructions")
st.markdown(scenario["instructions_en"])

# Preparation timer
if "start_chat" not in st.session_state:
    if st.button(" Start Preparation Timer (2 minutes)"):
        st.session_state.start_chat = False
        st.session_state.timer_start = time.time()

if "timer_start" in st.session_state and not st.session_state.get("start_chat", False):
    elapsed = time.time() - st.session_state.timer_start
    remaining = 30 - elapsed
    if remaining > 0:
        st.warning(f"Please prepare... Chat will start in {int(remaining)} seconds.")
        st.experimental_rerun()
    else:
        st.session_state.start_chat = True

# Chat begins
if st.session_state.get("start_chat", False):
    st.subheader("💬 Role-Play Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []
        # System message with assistant persona
        st.session_state.messages.append({
            "role": "system", "content": scenario["system_prompt"]
        })

    # Display previous messages
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            st.chat_message(msg["role"]).write(msg["content"])

    # User input
    user_input = st.chat_input("Enter your message here...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate assistant response
        with st.chat_message("assistant"):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=st.session_state.messages,
                temperature=0.7
            )
            reply = response.choices[0].message["content"]
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.markdown(reply)

    # Save & Show Dialogic Analysis
    if st.button("End Role-Play and Show Dialog Analysis"):
        st.subheader(" Sample Analysis")
        st.markdown(f"""
**Communication Type**: {scenario['type']}  
**User Role**: {scenario['social_role']['user']}  
**AI Role**: {scenario['social_role']['assistant']}  
**Compliance**: Dialogic turns showed high compliance with Grice’s maxims, especially relevance and manner.  
**Speech Acts**: Searle’s taxonomy revealed a mix of directives and commissives consistent with a {scenario['type']} frame.
        """)
        # Optionally: Add save logic here to file or database
