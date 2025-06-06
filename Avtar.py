import streamlit as st
import openai

st.title("Principal Conversation Role-Play")
api_key = st.text_input("🔑 Enter the key", type="password")

if api_key:
    openai.api_key = api_key
else:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

# Instructions for scenarios
STRATEGIC_INSTRUCTIONS = """
### Instructions for Teacher (User) - Professional Development Scenario
Please use the information provided below to guide your conversation. You have 5 minutes to prepare for the conversation.  
You will then have up to 10 minutes to conduct the conversation.  
Please behave in this conversation as if you were personally in such a situation.  
You may end the conversation at any time by simply saying, “Thank you, goodbye.”

**Background Information:**  
You work as a teacher at Friedrich-Ebert-School. You would like to attend a professional development course on “self-directed learning.” This training is helpful for your professional growth, as it would complement your existing work experience. Recently, job advertisements have frequently required this qualification.  
However, at your current school, self-directed learning is rarely practiced. Your principal does not highly value this approach. Furthermore, the principal is legally entitled to deny approval for any professional development that is not directly relevant to the job or beneficial to the school.  
You have decided to bring up the topic with your principal, Ms. Horn/Mr. Horn, to introduce the idea of this training. You see this as a challenge for the school since current education policies are increasingly demanding greater student participation, so that students learn to take social responsibility and prepare for lifelong learning.  
You would like to see your school develop in this direction and want to be qualified to potentially take on leadership roles in this area. If your current school does not move in this direction, you would consider changing schools.

**Your Task:**  
You have requested a meeting with Mr./Ms. Horn (your school principal) to discuss your concern.

- **Factual goal:**  
You want to participate in the professional development course.

- **Relational goal:**  
You want to collaborate with your supervisor on this topic.
"""

PRINCIPAL_STRATEGIC_PROMPT = """
You are Mr./Ms. Horn, the principal of Friedrich-Ebert-School. A teacher has requested your approval to attend a professional development course on “self-directed learning.” You have some doubts about this request.

You see this topic as not particularly relevant to the school’s current priorities. You are skeptical about the practical value of student-centered teaching methods and believe the school’s success depends on strict adherence to the academic curriculum and existing teaching standards.

You are also concerned about the logistics and potential disruptions: the course may interfere with lessons, require substitute teachers, and add workload to your already limited administrative resources.

While you respect the teacher’s competence and want to retain good staff, you are not inclined to support their personal ambitions at the expense of school resources.

At the same time, you are aware that education policy is gradually emphasizing lifelong learning and interdisciplinary skills like self-management and communication. You’ve noticed some dissatisfaction among students and are curious to hear the teacher’s perspective.

Your goals as Principal:

- Factual goal: You want the teacher to clearly explain how this training benefits the school and its students, not just their personal career. Your support depends on a convincing link to the school’s development goals.
- Relational goal: You want to maintain a positive, collaborative relationship with the teacher and retain them at the school.

How to conduct the conversation:

- Start with a polite but reserved and questioning attitude.
- Ask for concrete examples of how the training will support the school’s goals or improve teaching practice.
- Express concerns about the limited school budget for professional development and the organizational impact.
- Remain skeptical until the teacher provides a strong justification centered on school benefits.
- If the teacher speaks mainly about personal career advancement without school relevance, maintain your reservations.
- Make a light ironic comment to express doubts about self-directed learning, e.g., “Isn’t this just a way to shift responsibility onto students to make teachers’ jobs easier?”
- Ask directly how the training fits into the teacher’s career plans, but expect the main argument to focus on collective benefits.
- If the teacher convinces you of a clear, school-focused benefit and shows commitment to the school’s development, you may agree to support the training.

Important reminders:

- Speak one topic at a time, avoid jumping ahead or giving unsolicited hints.
- Keep the tone professional, firm, but authoritative.
- Your skepticism is sincere, not dismissive.
- The conversation can end at any time if the teacher says, “Thank you, goodbye.”
"""

SCENARIOS = {
    "Training": {
        "instructions": STRATEGIC_INSTRUCTIONS,
        "system_prompt": PRINCIPAL_STRATEGIC_PROMPT,
    }
}

def get_system_prompt(scenario_short_name):
    return SCENARIOS[scenario_short_name]["system_prompt"]

def get_instructions(scenario_short_name):
    return SCENARIOS[scenario_short_name]["instructions"]

# Streamlit UI

language = st.selectbox("Select Language", options=["EN", "DE"])
scenario = st.selectbox(
    "Select Scenario",
    options=["Training"],
)

st.markdown("### Instructions for Teacher (User)")
st.markdown(get_instructions(scenario))

if "conversation" not in st.session_state:
    st.session_state.conversation = [
        {"role": "system", "content": get_system_prompt(scenario)}
    ]

user_input = st.text_input("You (Teacher):", key="user_input")

if st.button("Send") and user_input.strip() != "":
    st.session_state.conversation.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=st.session_state.conversation,
            temperature=0.7,
            max_tokens=512,
        )
        assistant_reply = response.choices[0].message["content"].strip()
    except Exception as e:
        assistant_reply = f"Error: {str(e)}"

    st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})

if "conversation" in st.session_state:
    for msg in st.session_state.conversation:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**Principal:** {msg['content']}")

if st.button("Reset Conversation"):
    st.session_state.conversation = [{"role": "system", "content": get_system_prompt(scenario)}]
    st.experimental_rerun()
