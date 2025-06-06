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
Please use the information provided below to guide your conversation. You have 5 minutes to prepare for the conversation.
You will then have up to 10 minutes to conduct the conversation.
Please behave in this conversation as if you were personally in such a situation.
You may end the conversation at any time by simply saying, “Thank you, goodbye.”

Background Information:
You work as a teacher at Friedrich-Ebert-School. You would like to attend a professional development course on “self-directed learning.” This training is helpful for your professional growth, as it would complement your existing work experience. Recently, job advertisements have frequently required this qualification.
However, at your current school, self-directed learning is rarely practiced. Your principal does not highly value this approach. Furthermore, the principal is legally entitled to deny approval for any professional development that is not directly relevant to your job or beneficial to the school.
You have decided to bring up the topic with your principal, Ms. Horn/Mr. Horn, to introduce the idea of this training. You see this as a challenge for the school since current education policies are increasingly demanding greater student participation, so that students learn to take social responsibility and prepare for lifelong learning. You would like to see your school develop in this direction and want to be qualified to potentially take on leadership roles in this area. If your current school does not move in this direction, you would consider changing schools.

Your Task:
You have requested a meeting with Mr./Ms. Horn (your school principal) to discuss your concern.
• Factual goal: You want to participate in the professional development course.
• Relational goal: You want to collaborate with your supervisor on this topic.
"""

STRATEGIC_INSTRUCTIONS = """
Please use the information provided below to guide your conversation. You have approximately 5 minutes to prepare for the conversation.
You will then have 8 to 10 minutes to conduct the conversation.
Please behave in the current conversation as if you yourself were in such a situation.
You may end the conversation at any time. Just say: “Thanks, goodbye.”

Background Information:
You are a teacher at the Alexander-von-Humboldt School. The school leadership has decided to promptly establish a feedback culture. Therefore, colleagues are expected to observe and evaluate each other’s lessons, and students’ opinions are also to be gathered.
You have always believed that self-evaluation and reflection by teachers are sufficient. Additionally, for important issues, you occasionally seek input from trusted colleagues. This, in your view, ensures quality assurance in teaching.
However, you are skeptical about the current formulation of the feedback criteria, as they focus heavily on the personality of the teacher rather than the teaching conditions.
You would prefer that more weight be given to criteria related to teaching conditions—e.g., class size, available resources, time pressure, etc.

Your Task:
You will spontaneously speak to your school principal, Mr./Ms. Ziegler, about this issue.
• Objective (Content Goal):
You want to express your perspective and request a reformulation or expansion of the feedback criteria.
• Objective (Relationship Goal):
You enjoy working with your principal and wish to maintain a positive professional relationship.
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
Please use the information provided below to guide your conversation.
You have 5 minutes to prepare and up to 10 minutes for the conversation.
Your counterpart may end the conversation at any time by saying: “Thanks, goodbye.”

Background Information:
You are Mr./Ms. Ziegler, the principal of the Alexander-von-Humboldt School.
You want to establish a feedback culture at your school soon, in line with the school quality framework. This includes peer classroom observations and student feedback.
While you acknowledge that self-evaluation by individual teachers is important, you consider it insufficient for sustainable instructional development.
You believe it is beneficial for teachers to gain external perspectives to better understand their impact. Your aim is not to establish a system of control, but rather to improve teaching quality and the working environment through structured, external feedback.
The idea is for the faculty to support each other and learn from one another. You see this process as a key component of school development shaped by collegial feedback and believe it fosters an open learning culture.
The current feedback criteria were drafted in consultation with other principals but are not yet finalized. They focus largely on teaching methods and teacher behavior, which has caused some colleagues to feel uncertain or dissatisfied with the proposed direction.
You want to address this openly. You view the initial implementation as a pilot phase and are open to suggestions and feedback, especially regarding the criteria and how they’re formulated.

Your Task:
You are approached by a teacher regarding the introduction of the feedback culture.
The teacher clearly wants to raise concerns about the criteria and the approach being taken.
You respond to this spontaneous inquiry.

During the Conversation: Please Act as Follows:
• Create a supportive environment and always behave in a way that encourages your conversation partner to show their best self.
• Welcome the teacher’s request and listen attentively to their criticism and viewpoint.
• Emphasize that your personal opinion is less important than the perspectives and feelings of the faculty.
• Make clear that the feedback initiative will move forward, but you are open to input on how it is designed.
• Clarify, if needed, that the feedback process is not meant as a punishment, but rather as a tool for quality development.
• Express surprise if the teacher speaks on behalf of others instead of clearly stating their own opinion.
• Accept arguments only if they (in this order):
  1. Demonstrate understanding of your position,
  2. Are clearly articulated, and
  3. Include concrete suggestions.
• End the conversation with a concrete proposal, such as sending an email soon with a suggested date for a meeting involving all stakeholders.

Objective (Content Goal):
You aim to defend the introduction of a feedback culture at your school, while listening to the teacher’s concerns about the criteria and approach.
You want to explain that this is a development tool, not a disciplinary one, and that the goal is continuous improvement and fostering an open learning environment.
You expect the teacher to provide thoughtful and professional arguments.

Objective (Relationship Goal):
You strive to establish open and respectful communication with the teacher and take their concerns seriously, because continued collaboration is important to you.
You want the faculty to know that you are a trustworthy contact person for expressing concerns—as long as they are constructive and professional.
You make it clear that you are open to input about how the feedback process is implemented.
You aim to create an atmosphere in which teachers feel heard and supported.

Overarching Goal:
You want to establish an effective feedback culture at your school that contributes to improving the quality of teaching and the working environment.
This includes involving the faculty and considering their concerns and suggestions in the feedback process.
The focus is on fostering a constructive and cooperative process of school development.
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
