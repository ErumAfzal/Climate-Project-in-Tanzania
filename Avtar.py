import streamlit as st

# --- Instructions Texts ---

strategic_instructions = """
### Instruction for Teacher (User)

Please use the information provided below to guide your conversation. You have approximately 5 minutes to prepare for the conversation.  
You will then have 8 to 10 minutes to conduct the conversation.  
Please behave in the current conversation as if you yourself were in such a situation.  
You may end the conversation at any time. Just say: “Thanks, goodbye.”

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

understanding_instructions = """
### Instruction for the Role-Playing Person (Teacher) - User

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

**Type of communication:** Strategic communication  
**Social Role:** weak
"""

# --- Initialize session state ---

if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# --- Sidebar Controls ---

st.sidebar.title("Teacher-Principal Role-Play Chatbot")

language = st.sidebar.selectbox("Select Language", options=["English", "German"], index=0)

scenario = st.sidebar.selectbox(
    "Select Scenario",
    options=["Strategic", "Understanding"],
    index=0,
    help="Choose the communication style for the conversation."
)

input_type = st.sidebar.radio(
    "Select Input Type",
    options=["Text"],  # Audio disabled for now as requested
    index=0
)

st.sidebar.markdown("---")
st.sidebar.write("### Instructions")
if scenario == "Strategic":
    st.sidebar.markdown(strategic_instructions)
else:
    st.sidebar.markdown(understanding_instructions)

# --- Display the conversation ---

st.title("Teacher-Principal AI Role-Play Chatbot")

for i, chat in enumerate(st.session_state.conversation):
    role = chat['role']
    message = chat['message']
    if role == 'teacher':
        st.markdown(f"**Teacher:** {message}")
    else:
        st.markdown(f"**Principal:** {message}")

# --- Input box for user message ---

user_input = st.text_input("Your message (Teacher):", key="input")

if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter a message before sending.")
    else:
        # Add teacher message to conversation
        st.session_state.conversation.append({"role": "teacher", "message": user_input})

        # Simple AI Principal response logic depending on scenario

        def generate_principal_response(message, scenario):
            # For demo, basic keyword-based logic and canned responses aligned to scenario goals
            if "criteria" in message.lower() or "feedback" in message.lower():
                if scenario == "Strategic":
                    return (
                        "Thank you for sharing your perspective on the feedback criteria. "
                        "I agree that the teaching conditions should be considered. Let's work together to "
                        "expand the criteria and ensure a fair evaluation for all."
                    )
                else:
                    return (
                        "I understand your concerns about the current feedback process. "
                        "Let’s explore ways to collaboratively improve it while supporting your professional growth."
                    )
            elif "training" in message.lower() or "professional development" in message.lower():
                if scenario == "Understanding":
                    return (
                        "It's great that you want to pursue professional development. "
                        "I will consider your request carefully, keeping in mind the school's priorities."
                    )
                else:
                    return (
                        "I recognize the importance of professional development. "
                        "Let's discuss how it fits within our school's goals and resources."
                    )
            elif "thank" in message.lower():
                return "Thank you for the conversation. Goodbye!"
            else:
                # Generic fallback
                if scenario == "Strategic":
                    return "Let's continue discussing your concerns regarding teaching standards."
                else:
                    return "I appreciate your openness. Let's work together to find solutions."

        response = generate_principal_response(user_input, scenario)

        st.session_state.conversation.append({"role": "principal", "message": response})

        # Clear input box after sending
        st.experimental_rerun()
