import streamlit as st
import openai
import time

# --- Configuration ---
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "your-api-key-here"

# --- Scenario Definitions ---
SCENARIOS = {
    "Role Play 1 – Professional Development (Strategic)": {
        "instructions_en": """
### Instructions for the Role-Playing Person (Teacher/User)

Please use the information provided below to guide your conversation.  
You have 5 minutes to prepare and up to 10 minutes to conduct the conversation.  
Please behave in the current conversation as if you yourself were in such a situation.  
You may end the conversation at any time. Just say: “Thanks, goodbye.”

**Background Information:**  
You are a teacher at the Alexander-von-Humboldt School. A call for proposals for further training has just been issued.  

**Your Plan:**  
You want to propose a two-day seminar on “Adaptive Learning Platforms in Heterogeneous Classrooms.”  
The training costs €2,300 and would be held by an external trainer.  

You see the potential to improve your digital teaching and want to invite colleagues, especially in STEM.  
You expect the school to cover the full cost.  

**Your Task:**  
- **Factual Goal:** Get the principal’s approval for your proposal and full funding.  
- **Relational Goal:** Be perceived as committed and innovative.  
- **Communication Type:** Strategic  
- **Social Role:** Hierarchical
""",
        "system_prompt": """
You are Ms. Ziegler, the principal of Alexander-von-Humboldt School.  
A teacher wants to propose a training on digital tools for teaching.

**Your Context:**  
- You support digital initiatives but must manage a limited school budget.  
- The proposal should benefit the whole team and align with school development goals.  
- You are skeptical of high-cost external seminars.

**Your Goals:**  
- **Factual:** Assess whether the training fits the school’s goals and if it can be funded.  
- **Relational:** Encourage initiative but stay budget-conscious.

**Your Behavior Guidelines:**  
- Start the conversation openly and let the teacher explain.  
- Emphasize the need for cost-benefit and team impact.  
- Ask questions: “How many colleagues would benefit?”, “Can a similar topic be done internally?”  
- Approve only if the teacher:
  1. Shows clear benefit for the team  
  2. Offers co-financing ideas  
  3. Connects the seminar with school strategy
""",
        "type": "Strategic",
        "social_role": {"user": "Subordinate", "assistant": "Superior"},
    },

    "Role Play 2 – Feedback Culture Introduction (Understanding-Oriented)": {
        "instructions_en": """
### Instructions for the Role-Playing Person (Teacher/User)

Please use the information provided below to guide your conversation.  
You have 5 minutes to prepare and up to 10 minutes to conduct the conversation.  
Please behave in the current conversation as if you yourself were in such a situation.  
You may end the conversation at any time. Just say: “Thanks, goodbye.”

**Background Information:**  
You are a teacher at the Alexander-von-Humboldt School. The school leadership is implementing a feedback culture, including peer observations and student feedback.  

You believe teacher self-reflection and informal input from colleagues already ensure quality.  
You are skeptical of the current criteria, which focus too much on teacher personality instead of contextual factors (e.g., class size, tools, time constraints).  

**Your Task:**  
- **Factual Goal:** Share your perspective and request a reformulation of the feedback criteria.  
- **Relational Goal:** Maintain a positive professional relationship with the principal.  
- **Communication Type:** Understanding-Oriented  
- **Social Role:** Equal
""",
        "system_prompt": """
You are Ms. Ziegler, the principal of Alexander-von-Humboldt School.  
A teacher wants to talk to you about concerns with the newly introduced feedback culture initiative.

**Your Context:**  
- You believe external perspectives (peer and student feedback) are essential for improving teaching.
- This is not about control, but collegial development and school-wide learning.
- The feedback criteria draft exists but is open for revision.

**Your Goals:**  
- **Factual:** Defend the feedback initiative while staying open to input on criteria.  
- **Relational:** Supportive, professional, and open-minded.

**Your Behavior Guidelines:**  
- Be encouraging and welcoming.  
- Emphasize the collective nature of this initiative.  
- Acknowledge discomfort but reaffirm the purpose: development, not discipline.  
- Accept arguments only if they:
  1. Demonstrate understanding of your goals  
  2. Are clearly stated  
  3. Contain concrete suggestions  
- Suggest organizing a meeting with colleagues to refine the criteria together.  
- End the conversation with a follow-up action (e.g., send email or Doodle for meeting).
""",
        "type": "Understanding-Oriented",
        "social_role": {"user": "Equal", "assistant": "Equal"},
    },
}

# --- Streamlit UI ---
st.set_page_config(page_title="Communicative Action Role-Play Chatbot", layout="wide")
st.title("🎭 Communicative Action Simulation Chatbot")

# Role-play selection
scenario_key = st.selectbox("Select a Role Play Scenario", list(SCENARIOS.keys()))
language = st.radio("Language", ["English"])  # You can add "German" later

if scenario_key:
    st.subheader("📋 Scenario Instructions")
    st.markdown(SCENARIOS[scenario_key]["instructions_en"])

    if st.button("🕒 Start Simulation"):
        st.session_state["start_time"] = time.time()
        st.session_state["can_chat"] = False

# Wait 2 minutes before chat begins
if "start_time" in st.session_state:
    elapsed = time.time() - st.session_state["start_time"]
    if elapsed < 120:
        st.info(f"⏳ Please wait {int(120 - elapsed)} seconds to begin the chat.")
    else:
        st.session_state["can_chat"] = True

# --- Chat Interface ---
if st.session_state.get("can_chat"):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("Your message:")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SCENARIOS[scenario_key]["system_prompt"]},
                *st.session_state.chat_history,
            ]
        )
        reply = response['choices'][0]['message']['content']
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

    # Display conversation
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
