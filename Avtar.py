import streamlit as st

# Role-play scenarios with AI Principal responses and teacher instructions
SCENARIOS = {
    "Strategic": {
        "instructions_en": "Scenario: Strategic Communication. The Principal focuses on goal-oriented, outcome-driven dialogue. Emphasis on policy, control, and organizational objectives.",
        "instructions_de": "Szenario: Strategische Kommunikation. Die Schulleitung konzentriert sich auf zielorientierte, ergebnisgetriebene Dialoge. Schwerpunkt auf Richtlinien, Kontrolle und organisatorischen Zielen.",
        "responses_en": [
            "This feedback initiative is going to happen. It has already been decided.",
            "It’s no longer about whether we like it or not—it’s happening.",
            "But of course, you still have the opportunity to express your concerns and fears.",
            "We’ll find a solution. This isn’t meant to be a punishment—it’s about improving quality.",
        ],
        "responses_de": [
            "Diese Feedback-Initiative wird kommen. Es wurde bereits beschlossen.",
            "Es geht nicht mehr darum, ob es uns gefällt oder nicht – es passiert.",
            "Aber natürlich haben Sie weiterhin die Möglichkeit, Ihre Bedenken und Ängste zu äußern.",
            "Wir werden eine Lösung finden. Es soll keine Bestrafung sein – es geht um Qualitätsverbesserung.",
        ],
    },
    "Understanding-Oriented": {
        "instructions_en": "Scenario: Understanding-Oriented Communication. The Principal listens empathetically and focuses on shared meaning, mutual understanding, and collaboration.",
        "instructions_de": "Szenario: Verständigungsorientierte Kommunikation. Die Schulleitung hört empathisch zu und legt Wert auf gemeinsamen Sinn, gegenseitiges Verständnis und Zusammenarbeit.",
        "responses_en": [
            "I hear your concerns, and I understand your discomfort about being evaluated.",
            "This is not meant to punish you but to improve teaching quality together.",
            "Let’s work together to create a feedback process that includes all relevant factors.",
            "Your suggestions about including framework conditions are very valuable.",
        ],
        "responses_de": [
            "Ich höre Ihre Bedenken und verstehe Ihr Unbehagen bezüglich der Bewertung.",
            "Es soll Sie nicht bestrafen, sondern die Unterrichtsqualität gemeinsam verbessern.",
            "Lassen Sie uns gemeinsam einen Feedback-Prozess entwickeln, der alle relevanten Faktoren berücksichtigt.",
            "Ihre Vorschläge zur Einbeziehung der Rahmenbedingungen sind sehr wertvoll.",
        ],
    },
}

# Helper function to get next response based on turn count
def get_principal_response(scenario, language, turn):
    responses = SCENARIOS[scenario]["responses_en"] if language == "EN" else SCENARIOS[scenario]["responses_de"]
    if turn < len(responses):
        return responses[turn]
    else:
        # Repeat last response if turns exceed responses available
        return responses[-1]

st.set_page_config(page_title="Teacher-Principal Roleplay Chatbot", page_icon="🎭")

st.title("Teacher-Principal Roleplay Chatbot")

# Sidebar options
language = st.sidebar.radio("Select Language / Sprache wählen", ("EN", "DE"))
scenario = st.sidebar.radio("Select Scenario / Szenario wählen", ("Strategic", "Understanding-Oriented"))
input_type = "Text"  # Fixed as per your request

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Input type:** {input_type}")

# Show teacher instructions based on language and scenario
instructions_key = "instructions_en" if language == "EN" else "instructions_de"
st.info(SCENARIOS[scenario][instructions_key])

# Initialize session state for conversation logs and turn count
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "turn" not in st.session_state:
    st.session_state.turn = 0  # How many principal responses so far

# Chat input
teacher_input = st.text_input("Your message (Teacher) / Ihre Nachricht (Lehrer*in)")

if st.button("Send / Senden") and teacher_input.strip() != "":
    # Append teacher message
    st.session_state.conversation.append({"role": "Teacher", "text": teacher_input.strip()})

    # Get AI Principal response based on scenario, language, and turn count
    principal_response = get_principal_response(scenario, language, st.session_state.turn)
    st.session_state.conversation.append({"role": "Principal", "text": principal_response})

    st.session_state.turn += 1

# Display conversation log
for chat in st.session_state.conversation:
    if chat["role"] == "Teacher":
        st.markdown(f"**Teacher:** {chat['text']}")
    else:
        st.markdown(f"**Principal:** {chat['text']}")

# Button to clear conversation
if st.button("Clear Conversation / Gespräch löschen"):
    st.session_state.conversation = []
    st.session_state.turn = 0
    st.experimental_rerun()
