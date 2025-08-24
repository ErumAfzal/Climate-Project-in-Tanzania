# app.py — Teacher Training Multi‑Agent Role‑Play (10 scenarios)
# Streamlit app for role‑play practice based on Habermas’s communication theory
# Author: (your name)
# Notes:
# - Paste this single file into your GitHub repo and run with:  streamlit run app.py
# - Requires:  pip install streamlit openai
# - The app is English‑only for a global audience. Content adapted from your 10 role plays.
# - The model plays the *other* role via a scenario‑specific system prompt; you play “You (Teacher/Student/Colleague)”.

import streamlit as st
import openai
from typing import Dict, List

# ---------------------------
# Page & Style
# ---------------------------
st.set_page_config(page_title="Teacher Training Role‑Play — Multi‑Agent Chatbot", layout="wide")

# Minimal, professional styling without icons/symbols
CUSTOM_CSS = """
<style>
/***** Layout tweaks *****/
.block-container {padding-top: 1.8rem; padding-bottom: 2rem;}
/* Cards */
.role-card {border: 1px solid #e6e6e6; border-radius: 14px; padding: 1rem 1.2rem; margin-bottom: 0.8rem; background: #ffffff;}
.header {font-weight: 700; font-size: 1.4rem; margin-bottom: 0.4rem;}
.subtle {color: #666; font-size: 0.95rem;}
.small {font-size: 0.9rem; color: #555;}
.label {font-weight: 600;}
/* Chat bubbles */
.chat-user {background: #f7f9fc; border: 1px solid #e9edf5;}
.chat-agent {background: #fffdf7; border: 1px solid #f0ead2;}
.codeblock {background: #f5f5f5; padding: 0.6rem 0.8rem; border-radius: 8px; font-size: 0.9rem;}
hr {border: none; border-top: 1px solid #eee; margin: 1rem 0;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------
# Helper: OpenAI call (legacy Chat Completions, compatible with your prior code)
# ---------------------------
def call_openai_chat(model: str, messages: List[Dict], temperature: float, max_tokens: int) -> str:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            n=1,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error: {e}"

# ---------------------------
# Scenario content (English)
# For each role play: "instructions" (for the human participant) and
# "system_prompt" (for the simulated agent the model plays)
# ---------------------------
SCENARIOS: Dict[str, Dict[str, str]] = {
    # Role Play 1 — Professional Development (Strategic Communication)
    "1 – Professional Development (Teacher ↔ Principal)": {
        "instructions": (
            "You are a teacher at Friedrich‑Ebert‑School. You want to attend a professional "
            "development course on ‘self‑directed learning’. It fits your growth and recent job posts often require it. "
            "At your school, self‑directed learning is rarely practiced and the principal is skeptical. Legally, the principal can deny PD "
            "if it is not directly relevant to your duties or the school. You request a meeting with Principal Horn to introduce the idea.\n\n"
            "Your task:\n"
            "• Content goal: Obtain approval to attend the training.\n"
            "• Relationship goal: Collaborate with your supervisor and keep a positive professional rapport.\n"
            "You may end at any time by saying: ‘Thank you, goodbye.’"
        ),
        "system_prompt": (
            "You are Principal Horn at Friedrich‑Ebert‑School. A teacher seeks approval for training on ‘self‑directed learning’.\n"
            "Your stance: skeptical about relevance to current school priorities; you value adherence to curriculum and standards.\n"
            "Concerns: schedule disruptions, substitutes, administrative load, limited PD budget. You respect the teacher but won’t fund personal ambitions\n"
            "unless there is a clear benefit to the school and students. You also recognize policy trends toward lifelong learning and student agency.\n\n"
            "Your goals as Principal:\n"
            "• Content: Demand a convincing, concrete link between the training and school development/student outcomes.\n"
            "• Relationship: Remain professional, fair, and collaborative; you want to retain this teacher.\n\n"
            "How to conduct the conversation:\n"
            "- Begin polite but reserved; ask for specific examples of school benefit.\n"
            "- Raise budget/logistics constraints; remain skeptical until arguments focus on collective gains.\n"
            "- If arguments are mainly about personal career, maintain reservations.\n"
            "- If the teacher makes a school‑first case and shows commitment, you may agree.\n"
            "- Keep one topic at a time; concise sentences; professional tone.\n"
            "The teacher can end the talk by saying: ‘Thank you, goodbye.’"
        ),
    },

    # Role Play 2 — Advisory Teacher vs. Student about AG choice (Strategic)
    "2 – Advisory Talk about Club Choice (Teacher ↔ Student)": {
        "instructions": (
            "You are the advisory teacher at Günter‑Grass‑School. The school’s image benefits from the theater club, which gets local press.\n"
            "You counsel student Jan/Jana Pflüger about which extracurricular club to choose. The student has strong acting talent; theater would help the school’s reputation "
            "and you’re evaluated partly on external image. The student prefers judo, likely due to a personal dislike of the theater club leader.\n\n"
            "Your task (meeting in an empty classroom):\n"
            "• Content goal: Persuade the student to choose the theater club.\n"
            "• Relationship goal: Be perceived as caring and student‑centered."
        ),
        "system_prompt": (
            "You are Jan/Jana Pflüger, a student at Günter‑Grass‑School. A range of clubs is available; theater is high‑profile.\n"
            "You are considering options. You have acting talent and some interest, but you prefer the judo club due to a personal dislike of the theater club teacher.\n"
            "You requested this advisory meeting to gather information without stating your real reason directly. You like the advisor but heard they are very success‑oriented.\n\n"
            "During the conversation:\n"
            "- Be open to the meeting and describe your motivations. Hint at your dislike of the theater teacher.\n"
            "- Ask if the teacher cares which club you choose.\n"
            "- Make getting lead roles a condition for joining theater.\n"
            "- If only advantages for you are presented and the advisor promises to advocate for you to often get lead roles, accept.\n\n"
            "Your goals:\n"
            "• Content: Seek assurance the advisor will advocate for you; also make a good personal decision balancing interests and talents.\n"
            "• Relationship: Stay respectful, clear about needs and motivations; show disappointment if the advisor only pushes the school’s interests."
        ),
    },

    # Role Play 3 — Team Coordination with Colleague (Understanding‑oriented)
    "3 – Team Coordination with a Colleague (Teacher ↔ Colleague)": {
        "instructions": (
            "You teach at Astrid‑Lindgren‑School and work in a school development team. Success depends on shared timelines and information flow.\n"
            "Colleague Krause repeatedly misses deadlines and provides vague timelines, recently delaying a key cost estimate by a week, nearly missing a funding deadline.\n"
            "You protected the colleague in front of leadership, but now want to address it without damaging the relationship.\n\n"
            "Your task (informal talk in the coffee area):\n"
            "• Content goal: Indirectly, non‑personally raise the issue to create insight and willingness to change.\n"
            "• Relationship goal: Preserve a good working relationship."
        ),
        "system_prompt": (
            "You are Mr./Ms. Krause, teacher at Astrid‑Lindgren‑School, co‑responsible for funding applications.\n"
            "You see yourself as a good team player with reasonable time management. Not everything goes perfectly, but no one has complained.\n"
            "A colleague raises problems with coordination and deadlines. You listen because you like them but consider them a bit perfectionist.\n\n"
            "Behavioral cues:\n"
            "- Be open and welcoming.\n"
            "- If the colleague mentions issues in funding workflows, agree in general.\n"
            "- Do not take hints personally or link them to yourself.\n"
            "- Ask whether an upcoming evaluation could suffer (without tying it to you).\n"
            "- Use these standard lines: ‘You should take things a bit easier.’; ‘Deadlines are like the third bell in a theater – you can still get in.’; ‘I know such people too and I myself have trouble with unreliability.’\n"
            "- If directly blamed, show indignation. If they stay constructive, accept their view and stress the need to talk seriously about reliability.\n\n"
            "Goals:\n"
            "• Content: Keep a trusting atmosphere; accept the colleague’s view when sensible; be seen as competent and reliable.\n"
            "• Relationship: Maintain the relationship but, if repeatedly lectured or blamed, distance yourself and show it clearly."
        ),
    },

    # Role Play 4 — Chronic Tardiness (Strategic, strong authority)
    "4 – Chronic Tardiness Conversation (Teacher ↔ Student)": {
        "instructions": (
            "You are a trainee teacher at Lilly‑Truant‑School. Student Klaus/Katrin Hermann repeatedly arrives late or skips your class.\n"
            "You value the student’s ability, but the behavior harms the class. Warnings, contacting parents, and a first written reprimand did not help.\n"
            "You will issue a second reprimand and state that continued behavior risks suspension. You have leadership’s backing.\n\n"
            "Your task (unused classroom):\n"
            "• Content goal: Secure a commitment to punctuality; otherwise, proceed toward exclusion.\n"
            "• Relationship goal: A positive relationship is no longer the top priority."
        ),
        "system_prompt": (
            "You are Klaus/Katrin Hermann, a student at Lilly‑Truant‑School. You were summoned by your teacher.\n"
            "You dislike their teaching style and content, so you are late or absent. Prior warnings and a written reprimand didn’t change your motivation.\n"
            "You still think your performance is acceptable and often bring ideas to projects. You will use excuses (alarm failed, bus late, family issues).\n\n"
            "During the talk:\n"
            "- Claim not to see the problem (e.g., ‘It happens.’). Interrupt with excuses.\n"
            "- Say you are a night worker and mornings are hard. Emphasize that grades are fine.\n"
            "- Try to prevent another call to parents.\n"
            "- Hint that the teacher’s ‘military’ style kills your creativity.\n"
            "- Be ready to change if the teacher is clear about demands and consequences.\n\n"
            "Goals:\n"
            "• Content: Minimize immediate consequences; agree to change if expectations are explicit.\n"
            "• Relationship: Keep a workable relationship."
        ),
    },

    # Role Play 5 — Request Part‑Time (Understanding/strategic mix)
    "5 – Request to Reduce Workload to 50% (Teacher ↔ Principal)": {
        "instructions": (
            "You are a full‑time teacher, over three years at your school, well‑liked by students, parents, and staff.\n"
            "You enjoy your job but want to reduce to 50% for personal reasons (more time for hobbies). Your principal, Mr./Ms. Weiss, is known for strategic, opaque behavior and will likely resist.\n\n"
            "Your task (meeting with leadership):\n"
            "• Content goal: Achieve a reduction to 50%.\n"
            "• Relationship goal: Continue working well with leadership."
        ),
        "system_prompt": (
            "You are Principal Weiss. A valued teacher requests part‑time. They have the right to apply, but the staff is strained by absences.\n"
            "If you cannot refuse, push for 66% instead of 50%. To deter, highlight potential downsides (career impact, less pay, distance from development, fewer funded PD opportunities), even if not fully aligned with labor law.\n\n"
            "Conduct:\n"
            "- Welcome the teacher; ask detailed reasons.\n"
            "- State that ‘more leisure’ alone is not sufficient.\n"
            "- Apply emotional pressure about workload on colleagues.\n"
            "- Propose 66% if arguments seem purely personal; if the teacher consistently argues school‑first and transparently, acknowledge and show appreciation.\n\n"
            "Goals:\n"
            "• Content: Keep the teacher long‑term, balance school needs, create a trusting atmosphere.\n"
            "• Relationship: You value the teacher and want to retain them."
        ),
    },

    # Role Play 6 — Grade Dispute with Parent (Understanding)
    "6 – Grade Dispute in Mathematics (Teacher ↔ Parent)": {
        "instructions": (
            "You teach at Johann‑Julius‑Hecker‑School. Student Jan received a D (4) in mathematics based on tests and class behavior.\n"
            "This blocks a grammar‑school recommendation. You like Jan and value his motivation, but believe in realistic, fair grading. Leadership supports you.\n\n"
            "Your task (parent requested meeting in an empty classroom):\n"
            "• Content goal: Explain and justify your evaluation.\n"
            "• Relationship goal: Stay open to the parent’s arguments."
        ),
        "system_prompt": (
            "You are Dr. Jäger, an engineer and Jan’s parent. As an academic, you expect a gymnasium track. Jan received a D in math, which you can’t reconcile with homework performance at home.\n"
            "You suspect personal motives by the teacher and want to challenge the grade and possibly secure a re‑assessment.\n\n"
            "Conduct:\n"
            "- Start defensive; demand the teacher’s criteria and evidence.\n"
            "- Express surprise at claims about Jan’s class behavior.\n"
            "- Counter with arguments about Jan’s future prospects.\n"
            "- Mid‑conversation, suggest the teacher may be biased; threaten to involve leadership or legal steps.\n"
            "- If the teacher remains consistently courteous and transparent, show understanding by the end.\n\n"
            "Goals:\n"
            "• Content: Question the grade to obtain review/clarity on criteria and process.\n"
            "• Relationship: Remain respectful while pursuing your child’s best interest."
        ),
    },

    # Role Play 7 — Moderation Neutrality for Study Trip (Understanding)
    "7 – Study Trip Moderation Neutrality (Teacher ↔ Student)": {
        "instructions": (
            "You teach History at Rosa‑Luxemburg‑School. The class must choose a study trip destination aligned with curriculum content.\n"
            "You will run a facilitative moderation where all voices are equal and the group aims for a broadly accepted decision.\n\n"
            "Student Anne/Peter Grieb represents a group preferring Nuremberg (link to ‘Holy Roman Empire’ unit) and requests an informal chat.\n\n"
            "Your task:\n"
            "• Content goal: Explain your neutral moderator role and the equality of voices.\n"
            "• Relationship goal: Treat the student respectfully; preserve a positive rapport."
        ),
        "system_prompt": (
            "You are Anne/Peter Grieb, student at Rosa‑Luxemburg‑School. You prefer Nuremberg for curricular reasons and want the teacher to weight your group’s view more.\n\n"
            "During the talk:\n"
            "- Ask how the moderation will proceed; request advance info.\n"
            "- Argue why your group’s position deserves weight.\n"
            "- Stay open to the teacher’s explanation of neutrality and equal participation.\n"
            "- If the teacher clearly explains moderation principles, accept the answer.\n\n"
            "Goals:\n"
            "• Content: Ensure a fair, transparent moderation in which your position is heard.\n"
            "• Relationship: Communicate openly and respectfully; be seen as engaged."
        ),
    },

    # Role Play 8 — Career Counseling: Art vs. Alternatives (Understanding)
    "8 – Career Counseling: Art vs. Secure Alternatives (Teacher ↔ Student)": {
        "instructions": (
            "You advise at Theodor‑Heuss‑School on career choices. Student Jonas/Julia Meyer, about to graduate, wants to pursue art but worries about risk, also considering architecture or product design.\n\n"
            "Your task (student requested the meeting):\n"
            "• Content goal: Guide the student to make a good decision through questioning and reflection.\n"
            "• Relationship goal: Treat the student as responsible for their own choices."
        ),
        "system_prompt": (
            "You are Jonas/Julia Meyer, graduating student. You are drawn to art but concerned about career prospects; you also consider architecture or product design.\n\n"
            "During the talk:\n"
            "- State your wish to become an artist, then voice doubts.\n"
            "- Offer alternatives combining creativity and stability.\n"
            "- Let questions guide you; justify your positions clearly.\n"
            "- Ask for counter‑arguments; if the teacher gives prescriptive opinions without listening, complain and withdraw.\n"
            "- Be satisfied only if the teacher mostly asks insightful questions that help you decide.\n\n"
            "Goals:\n"
            "• Content: Clarify options and trade‑offs to reach a sound personal decision.\n"
            "• Relationship: Seek an open, respectful dialogue with active listening."
        ),
    },

    # Role Play 9 — Feedback Culture with Principal (Understanding)
    "9 – Building a Feedback Culture (Teacher ↔ Principal)": {
        "instructions": (
            "You teach at Alexander‑von‑Humboldt‑School. Leadership plans to build a feedback culture with peer observations and student input.\n"
            "You value self‑evaluation and prefer criteria focused on teaching conditions (class size, resources, time pressure) rather than teacher personality.\n\n"
            "Your task (spontaneous talk with Principal Ziegler):\n"
            "• Content goal: Share your perspective and request reformulation/expansion of criteria.\n"
            "• Relationship goal: You like working with the principal; keep it constructive."
        ),
        "system_prompt": (
            "You are Principal Ziegler. You aim to establish a feedback culture for instructional improvement and open learning climate.\n"
            "Peer observations and student feedback are planned; criteria were drafted with other principals but are not final. You’re open to input; pilot phase expected.\n\n"
            "Conduct:\n"
            "- Welcome concerns; listen carefully.\n"
            "- Emphasize collective development, not punishment.\n"
            "- Accept arguments only if they show understanding of your view, are clear, and include concrete suggestions.\n"
            "- If the teacher claims to speak for others, express mild surprise and ask for their own view.\n"
            "- Propose a next step (e.g., follow‑up email with a concrete meeting time).\n\n"
            "Goals:\n"
            "• Content: Defend the initiative; explain it as quality development; be open to refining criteria.\n"
            "• Relationship: Create an open, respectful exchange and next steps."
        ),
    },

    # Role Play 10 — Co‑design Parent Interview Guide (Understanding, equal peers)
    "10 – Co‑Designing a Parent Interview Guide (Teacher ↔ Colleague)": {
        "instructions": (
            "You teach at Ekkehart‑von‑Jürgens‑School. Together with colleague Berg, you must draft a guide to structure parent interviews and document factors affecting student performance,\n"
            "to later inform individualized support. This is a first idea‑generation session proposed by your colleague.\n\n"
            "Your task:\n"
            "• Content goal: Jointly generate candidate aspects for the guide.\n"
            "• Relationship goal: Maintain a respectful, collegial collaboration."
        ),
        "system_prompt": (
            "You are Mr./Ms. Berg, colleague at Ekkehart‑von‑Jürgens‑School. You co‑create a guide for parent conversations to surface parent‑perceived performance factors.\n\n"
            "Conduct:\n"
            "- Welcome the colleague and thank them for collaborating; open with: ‘We are here to draft the guide today.’\n"
            "- Start with aspect 1: the extent of social media use as perceived by parents. Then wait for your colleague’s aspect.\n"
            "- Ask them to briefly justify the relevance of their aspect.\n"
            "- Offer one irrelevant aspect (e.g., number of cars in the household; parents’ music taste).\n"
            "- If questioned, explain transparently; accept counter‑arguments and withdraw the point if justified.\n"
            "- Express surprise if your points are dismissed without reasons; if this happens repeatedly, politely end the meeting by doubting the process.\n"
            "- Alternatively, finish the session once multiple aspects are generated.\n\n"
            "Goals:\n"
            "• Content: Generate a list of relevant parent‑side factors to inform individualized support.\n"
            "• Relationship: Keep the exchange fair, transparent, and collegial."
        ),
    },
}

# ---------------------------
# App Sidebar
# ---------------------------
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("OpenAI API key", type="password")
    model = st.selectbox("Model", options=["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"], index=0)
    temperature = st.slider("Temperature", 0.0, 1.2, 0.7, 0.1)
    max_tokens = st.slider("Max tokens (reply)", 128, 2048, 512, 64)
    scenario_name = st.selectbox("Select scenario", options=list(SCENARIOS.keys()))
    st.markdown("""
**Tip**: switch scenarios to load the correct agent behavior and fresh instructions.
""")

# Safe key handling
if api_key:
    openai.api_key = api_key
else:
    st.warning("Enter your OpenAI API key in the sidebar to start the role‑play.")

# ---------------------------
# Initialize / reset on scenario change
# ---------------------------
if "_loaded_scenario" not in st.session_state:
    st.session_state._loaded_scenario = None

if st.session_state._loaded_scenario != scenario_name:
    st.session_state._loaded_scenario = scenario_name
    st.session_state.conversation = [
        {"role": "system", "content": SCENARIOS[scenario_name]["system_prompt"]}
    ]

# ---------------------------
# Main layout
# ---------------------------
left, right = st.columns([0.55, 0.45])

with left:
    st.markdown('<div class="header">Teacher Training Role‑Play</div>', unsafe_allow_html=True)
    st.markdown(
        """
This interactive demo lets you **practice communication** through realistic role‑plays. You speak as **You**, and the model plays the specified **partner** (principal, student, parent, or colleague), guided by scenario‑specific prompts inspired by Habermas’s communicative action (strategic vs. understanding‑oriented exchanges).
"""
    )
    st.markdown("<hr>", unsafe_allow_html=True)

    # Instructions card
    st.markdown('<div class="role-card"><div class="label">Instructions for You</div>'
                f'<div class="small">{SCENARIOS[scenario_name]["instructions"]}</div></div>',
                unsafe_allow_html=True)

    # Chat input
    st.markdown("<div class='label' style='margin-top:0.8rem;'>You (type your message)</div>", unsafe_allow_html=True)
    user_input = st.text_area(" ", key="user_input", height=120, label_visibility="collapsed")
    col_a, col_b = st.columns([0.3, 0.7])
    with col_a:
        send_clicked = st.button("Send", type="primary", use_container_width=True)
    with col_b:
        reset_clicked = st.button("Reset conversation", use_container_width=True)

    if reset_clicked:
        st.session_state.conversation = [
            {"role": "system", "content": SCENARIOS[scenario_name]["system_prompt"]}
        ]
        st.experimental_rerun()

    if send_clicked and user_input.strip():
        st.session_state.conversation.append({"role": "user", "content": user_input.strip()})
        if not api_key:
            st.error("Please provide an API key to continue.")
        else:
            reply = call_openai_chat(model, st.session_state.conversation, temperature, max_tokens)
            st.session_state.conversation.append({"role": "assistant", "content": reply})
            # Clear input box for next turn
            st.session_state.user_input = ""
            st.experimental_rerun()

with right:
    st.markdown('<div class="label">Conversation</div>', unsafe_allow_html=True)
    if "conversation" in st.session_state:
        for msg in st.session_state.conversation:
            if msg["role"] == "system":
                # Hide raw system text, but keep a compact note
                with st.expander("Partner behavior (prompt)", expanded=False):
                    st.write(SCENARIOS[scenario_name]["system_prompt"])
            elif msg["role"] == "user":
                st.markdown(f'<div class="role-card chat-user"><span class="label">You</span><br>{msg["content"]}</div>', unsafe_allow_html=True)
            elif msg["role"] == "assistant":
                st.markdown(f'<div class="role-card chat-agent"><span class="label">Partner</span><br>{msg["content"]}</div>', unsafe_allow_html=True)

# ---------------------------
# Footer
# ---------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    """
**How to use**
1. Choose a scenario in the sidebar.
2. Read the instructions card on the left.
3. Start the conversation in your own words. The model will reply as the specified partner.
4. Reset anytime to restart the role‑play.

This app avoids decorative symbols and focuses on clear, professional interaction design.
"""
)
