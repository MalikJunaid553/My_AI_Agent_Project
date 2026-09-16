import streamlit as st
import requests

st.set_page_config(
    page_title="AI Agent | Web Search & Email",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_URL = "https://myaiagentproject-production.up.railway.app/api/v1/chat"


st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(92, 45, 255, 0.30), transparent 30%),
        radial-gradient(circle at 90% 15%, rgba(0, 220, 255, 0.20), transparent 28%),
        radial-gradient(circle at 50% 90%, rgba(255, 0, 170, 0.16), transparent 30%),
        linear-gradient(135deg, #05051b 0%, #0b0b32 45%, #090522 100%);
    color: white;
}

.block-container {
    max-width: 1100px;
    padding-top: 3rem;
    padding-bottom: 4rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

section[data-testid="stSidebar"] {
    display: none;
}

/* HERO */

.hero {
    text-align: center;
    padding: 25px 20px 35px 20px;
}

.robot {
    font-size: 70px;
    margin-bottom: 5px;
}

.hero h1 {
    font-size: 64px;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(90deg, #00eaff, #8b5cf6, #ff3cac);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 23px;
    font-weight: 700;
    margin-top: 12px;
    color: #55e7ff;
}

.hero-description {
    max-width: 720px;
    margin: 15px auto 0 auto;
    color: #d5d7f7;
    font-size: 17px;
    line-height: 1.7;
}

/* GLOW LINE */

.glow-line {
    width: 150px;
    height: 4px;
    margin: 25px auto;
    border-radius: 20px;
    background: linear-gradient(90deg, #00eaff, #8b5cf6, #ff3cac);
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.8);
}

/* SECTION */

.section-title {
    text-align: center;
    font-size: 28px;
    font-weight: 800;
    margin: 25px 0 22px 0;
}

.section-description {
    text-align: center;
    color: #bfc3e7;
    margin-bottom: 25px;
}

/* HOW IT WORKS */

.step-card {
    min-height: 240px;
    padding: 25px 18px;
    border-radius: 22px;
    background: rgba(255,255,255,0.075);
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(18px);
    text-align: center;
    box-shadow: 0 15px 40px rgba(0,0,0,0.25);
}

.step-number {
    display: inline-flex;
    width: 38px;
    height: 38px;
    border-radius: 50%;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    background: linear-gradient(135deg, #7c3aed, #ec4899);
    margin-bottom: 12px;
}

.step-icon {
    font-size: 42px;
}

.step-card h3 {
    font-size: 18px;
    margin: 12px 0 8px 0;
}

.step-card p {
    color: #bfc3e7;
    font-size: 14px;
    line-height: 1.6;
}

/* ACCURACY CARD */

.accuracy {
    margin: 25px auto 45px auto;
    max-width: 700px;
    text-align: center;
    padding: 15px 20px;
    border-radius: 18px;
    background: rgba(0, 220, 255, 0.08);
    border: 1px solid rgba(0, 220, 255, 0.25);
    color: #bdf7ff;
}

/* CHAT */

.chat-wrapper {
    padding: 30px;
    border-radius: 28px;
    background: rgba(255,255,255,0.065);
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(20px);
    box-shadow: 0 25px 70px rgba(0,0,0,0.35);
}

.chat-title {
    font-size: 25px;
    font-weight: 800;
    margin-bottom: 25px;
}

/* CHAT MESSAGES */

.user-message {
    display: flex;
    justify-content: flex-end;
    margin: 15px 0;
}

.user-bubble {
    max-width: 75%;
    padding: 14px 18px;
    border-radius: 20px 20px 5px 20px;
    background: linear-gradient(135deg, #6d28d9, #db2777);
    color: white;
    box-shadow: 0 8px 25px rgba(124, 58, 237, 0.25);
}

.assistant-message {
    display: flex;
    justify-content: flex-start;
    margin: 15px 0;
}

.assistant-bubble {
    max-width: 82%;
    padding: 16px 19px;
    border-radius: 20px 20px 20px 5px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color: #f1f3ff;
    line-height: 1.6;
}

/* TECH STACK */

.tech-card {
    text-align: center;
    padding: 18px;
    border-radius: 18px;
    background: rgba(255,255,255,0.065);
    border: 1px solid rgba(255,255,255,0.12);
    color: #e8eaff;
    font-weight: 600;
}

/* INPUT */

div[data-testid="stTextInput"] input,
div[data-testid="stTextInput"] input[type="text"] {
    background-color: #171735 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    caret-color: #00eaff !important;
    border: 1px solid rgba(139, 92, 246, 0.6) !important;
    border-radius: 16px !important;
    padding: 15px !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #9da2c8 !important;
    opacity: 1 !important;
}

div[data-testid="stTextInput"] input:focus {
    background-color: #171735 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border-color: #00eaff !important;
    box-shadow: 0 0 15px rgba(0, 234, 255, 0.25) !important;
}

.stButton > button {
    width: 100%;
    height: 52px;
    border: none;
    border-radius: 16px;
    font-weight: 800;
    font-size: 16px;
    color: white;
    background: linear-gradient(135deg, #2563eb, #9333ea, #ec4899);
    box-shadow: 0 8px 25px rgba(124,58,237,0.35);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(124,58,237,0.55);
}

/* FOOTER */

.footer {
    text-align: center;
    margin-top: 55px;
    color: #8f94bd;
    font-size: 14px;
}

.footer strong {
    color: #4deaff;
}

</style>
""", unsafe_allow_html=True)


# -------------------------
# SESSION STATE
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------------
# HERO
# -------------------------

st.html("""
<div class="hero">

    <div class="robot">🤖</div>

    <h1>AI Assistant</h1>

    <div class="hero-subtitle">
        Search the Web • Get Answers • Send Emails
    </div>

    <div class="hero-description">
        An AI-powered agent that understands your request, searches the
        live internet when needed, processes the information, and can
        deliver the results directly to your inbox.
    </div>

    <div class="glow-line"></div>

</div>
""")


# -------------------------
# HOW IT WORKS
# -------------------------

st.markdown(
    '<div class="section-title">✨ How It Works</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">A look behind the scenes of this AI agent.</div>',
    unsafe_allow_html=True
)

steps = [
    ("1", "💬", "You Ask",
     "Type a question or request in the chat."),
    ("2", "🔎", "AI Searches",
     "The agent decides when it needs live internet information."),
    ("3", "📄", "Gets Information",
     "The search results are read and processed by the AI."),
    ("4", "📧", "Sends Email",
     "If you ask for an email, the agent sends the information."),
    ("5", "✅", "Done",
     "You receive the answer here or in your inbox.")
]

cols = st.columns(5)

for col, step in zip(cols, steps):
    with col:
        st.markdown(
            f"""
            <div class="step-card">
                <div class="step-number">{step[0]}</div>
                <div class="step-icon">{step[1]}</div>
                <h3>{step[2]}</h3>
                <p>{step[3]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("""
<div class="accuracy">
    🛡️ <strong>Reliable by design</strong> —
    the agent uses actual search results instead of inventing live information.
</div>
""", unsafe_allow_html=True)


# -------------------------
# CHAT
# -------------------------

st.html("""
<div class="chat-wrapper">
    <div class="chat-title">
        💬 Chat with the AI Assistant
    </div>
</div>
""")


# Display previous messages

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
                <div class="user-bubble">
                    {message["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="assistant-message">
                <div class="assistant-bubble">
                    🤖 {message["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# -------------------------
# SEND FUNCTION
# -------------------------

def send_message():

    message = st.session_state.message_input.strip()

    if not message:
        return

    st.session_state.messages.append({
        "role": "user",
        "content": message
    })

    try:

        with st.spinner("🤖 AI agent is working..."):

            response = requests.post(
                API_URL,
                json={"prompt": message},
                timeout=120
            )

        if response.status_code == 200:

            data = response.json()

            answer = data.get("output", "The agent did not return a response.")

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        else:

            st.session_state.messages.append({
                "role": "assistant",
                "content": f"⚠️ Backend returned an error: {response.status_code}"
            })

    except requests.exceptions.RequestException:

        st.session_state.messages.append({
            "role": "assistant",
            "content": "⚠️ Something went wrong while contacting the AI agent."
        })

    st.session_state.message_input = ""


# -------------------------
# INPUT
# -------------------------

st.text_input(
    "Message",
    placeholder="Ask me anything... e.g. What's Apple's stock price today?",
    key="message_input",
    label_visibility="collapsed",
    on_change=send_message
)

st.button(
    "🚀 Send",
    on_click=send_message
)

st.markdown(
    '<div style="text-align:center;color:#9da2c8;margin-top:8px;">Press Enter to send • Or click Send</div>',
    unsafe_allow_html=True
)


# -------------------------
# TECH STACK
# -------------------------

st.markdown(
    '<div class="section-title" style="margin-top:60px;">⚡ Tech Stack</div>',
    unsafe_allow_html=True
)

tech = [
    "🐍 Python",
    "🧠 LangGraph",
    "⚡ FastAPI",
    "🎈 Streamlit",
    "🔌 MCP / FastMCP",
    "📧 Gmail / Yagmail"
]

cols = st.columns(6)

for col, item in zip(cols, tech):
    with col:
        st.markdown(
            f'<div class="tech-card">{item}</div>',
            unsafe_allow_html=True
        )


# -------------------------
# FOOTER
# -------------------------

st.markdown("""
<div class="footer">
    Built with ❤️, Python, AI and lots of ☕
    <br><br>
    <strong>AI Agent Portfolio Project</strong>
</div>
""", unsafe_allow_html=True)