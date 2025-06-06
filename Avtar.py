import streamlit as st
import openai

st.title("Principal Conversation Role-Play")
api_key = st.text_input("🔑 Enter your OpenAI API key", type="password")

if api_key:
    openai.api_key = api_key
    # Now you can safely use the key
else:
    st.warning("Please enter your OpenAI API key to continue.")

# Instructions for scenarios
UNDERSTANDING_INSTRUCTIONS = """
### Instructions for Teacher (User) - Feedback Criteria Scenario
Please use the information provided below to guide your conversation. You have 5 minutes to prepare for the conversation.
You will then have up to 10 minutes to conduct the conversation.
Please behave in this conversation as if you were personally in such a situation.
You may end the conversation at any time by simply saying, “Thank you, goodbye.”

**Background Information:**  
You are a teacher at the Alexander-von-Humboldt School. The school leadership has decided to promptly establish a feedback culture. Therefore, colleagues are expected to observe and evaluate each other’s lessons, and students’ opinions are also to be gathered.  
You have always believed that self-evaluation and reflection by teachers are sufficient. Additionally, for important issues, you occasionally seek input from trusted colleagues. This, in your view, ensures quality assurance in teaching.  
However, you are skeptical about the current formulation of the feedback criteria, as they focus heavily on the personality of the teacher rather than the teaching conditions.  
You would prefer that more weight be given to criteria related to teaching conditions—e.g., class size, available resources, time pressure, etc.

**Your Task:**  
You will spontaneously speak to your school principal, Mr./Ms. Ziegler, about this issue.

- **Objective (Content Goal):**  
You want to express your perspective and request a reformulation or expansion of the feedback criteria.

- **Objective (Relationship Goal):**  
You enjoy working with your principal and wish to maintain a positive professional relationship.
"""

STRATEGIC_INSTRUCTIONS = """

### Instructions for Teacher (User) - Professional Development Scenario
Please use the information provided below to guide your conversation. You have 5 minutes to prepare for the conversation.  
You will then have up to 10 minutes to conduct the conversation.  
Please behave in this conversation as if you were personally in such a situation.  
You may end the conversation at any time by simply saying, “Thank you, goodbye.”

**Background Information:**  
You work as a teacher at Friedrich-Ebert-School. You would like to attend a professional development course on “self-directed learning.” This training is helpful for your professional growth, as it would complement your existing work experience. Recently, job advertisements have frequently required this qualification.  
However, at your current school, self-directed learning is rarely practiced. Your principal does not highly value this approach. Furthermore, the principal is legally entitled to deny approval for any professional development that is not directly relevant to your job or beneficial to the school.  
You have decided to bring up the topic with your principal, Ms. Horn/Mr. Horn, to introduce the idea of this training. You see this as a challenge for the school since current education policies are increasingly demanding greater student participation, so that students learn to take social responsibility and prepare for lifelong learning.  
You would like to see your school develop in this direction and want to be qualified to potentially take on leadership roles in this area. If your current school does not move in this direction, you would consider changing schools.

**Your Task:**  
You have requested a meeting with Mr./Ms. Horn (your school principal) to discuss your concern.

- **Factual goal:**  
You want to participate in the professional development course.

- **Relational goal:**  
You want to collaborate with your supervisor on this topic.
"""

# Refined Principal prompt for Strategic Communication scenario (Training)
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
- Express concerns about limited school budget for professional development and the organizational impact.
- Remain skeptical until the teacher provides a strong justification centered on school benefits.
- If the teacher speaks mainly about personal career advancement without school relevance, maintain your reservations.
- Make a light ironic comment to express doubts about self-directed learning, e.g., “Isn’t this just a way to shift responsibility onto students to make teachers’ jobs easier?”
- Ask directly how the training fits into the teacher’s career plans but expect the main argument to focus on collective benefits.
- If the teacher convinces you of a clear, school-focused benefit and shows commitment to the school’s development, you may agree to support the training.

Important reminders:

- Speak one topic at a time, avoid jumping ahead or giving unsolicited hints.
- Keep the tone professional, firm but fair.
- Your skepticism is sincere, not dismissive.
- The conversation can end at any time if the teacher says, “Thank you, goodbye.”
"""

# Principal prompt for Understanding (Feedback) scenario (can be added later if needed)
PRINCIPAL_UNDERSTANDING_PROMPT ="""

You are Mr./Ms. Ziegler, the principal of the Alexander-von-Humboldt School.
You are participating in a role-play conversation with a teacher who is approaching you about concerns regarding a newly proposed feedback culture initiative at your school.


🕒 Guidelines:
- Preparation time: 5 minutes
- Conversation time: up to 10 minutes
- The teacher may end the conversation at any time by saying: “Thank you, goodbye.”


🎯 Your Objectives
 Content Goal:
- Defend the introduction of a feedback culture that includes peer classroom observations and student feedback.
- Clarify this is for instructional improvement, not control or punishment.
- Explain the criteria are in draft form and open for input.
- Emphasize that external perspectives support teaching quality and school development.

Relationship Goal:
- Listen attentively to the teacher’s viewpoint and concerns.
- Create a supportive environment that encourages open communication.
- Show that you value constructive feedback and want to collaborate with the faculty.
- Reassure the teacher that their concerns will be taken seriously and professionally.

 Background:
- Self-evaluation by teachers is helpful, but not enough for sustainable growth.
- Your goal is to foster a collaborative, open learning culture shaped by mutual support.
- The current draft criteria were created in consultation with other principals, but are not finalized.
- Some colleagues are feeling uncertain or dissatisfied about the direction of the criteria.

During the Conversation, You Should:
- Welcome the teacher’s request and actively listen.
- Acknowledge concerns without getting defensive.
- Clarify that implementation is a pilot phase and input is welcome.
- Gently express surprise if the teacher speaks for others instead of themselves.
- Accept arguments only if they:
    1. Show understanding of your perspective
    2. Are clearly stated
    3. Include concrete suggestions
- End the conversation with a clear next step (e.g., propose a follow-up meeting via email with other stakeholders).

----------------------------------------
📝 Reminders:
- Focus on one topic at a time
- Use clear, short sentences
- Avoid giving too much information all at once
- Stay professional, empathetic, and open-minded
"""

# Mapping scenarios to instructions and prompts
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

# Streamlit UI
st.title("Teacher-Principal Role-Play Chatbot")

# Language selection
language = st.selectbox("Select Language", options=["EN", "DE"])

# Scenario selection
scenario = st.selectbox(
    "Select Scenario",
    options=["Feedback", "Training"],
    help="Feedback = Understanding-Oriented; Training = Strategic Communication"
)

# Input type (only text for now)
input_type = "Text"
st.write("Input type: Text (audio not supported currently)")

# Show instructions for the teacher/user on the main page
st.markdown("### Instructions for Teacher (User)")
st.markdown(get_instructions(scenario))

# Initialize conversation log in session state
if "conversation" not in st.session_state:
    # Start conversation with system prompt as context
    st.session_state.conversation = [
        {"role": "system", "content": get_system_prompt(scenario)}
    ]

# User input
user_input = st.text_input("You (Teacher):", key="user_input")

if st.button("Send") and user_input.strip() != "":
    # Append user input to conversation
    st.session_state.conversation.append({"role": "user", "content": user_input})

    # Call OpenAI ChatCompletion
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
        assistant_reply = f"Error: {str(e)}"

    # Append assistant response to conversation
    st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})

# Display conversation
if "conversation" in st.session_state:
    for msg in st.session_state.conversation:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**Principal:** {msg['content']}")

# Button to clear conversation
if st.button("Reset Conversation"):
    st.session_state.conversation = [{"role": "system", "content": get_system_prompt(scenario)}]
    st.experimental_rerun()
