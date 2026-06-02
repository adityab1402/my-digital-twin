import streamlit as st
import google.generativeai as genai
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from datetime import datetime
import time

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Aditya Bambole | Digital Twin",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Root Variables ── */
:root {
    --bg-primary: #070B14;
    --bg-card: #0D1220;
    --bg-glass: rgba(255,255,255,0.04);
    --accent: #4F9EFF;
    --accent-warm: #FF6B35;
    --accent-green: #00E5A0;
    --text-primary: #F0F4FF;
    --text-muted: #8892A4;
    --border: rgba(79,158,255,0.15);
    --glow: rgba(79,158,255,0.25);
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

.stApp {
    background: var(--bg-primary) !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% 0%, rgba(79,158,255,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(0,229,160,0.05) 0%, transparent 60%) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Profile Card ── */
.profile-card {
    background: linear-gradient(135deg, rgba(79,158,255,0.12), rgba(0,229,160,0.06));
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px 20px;
    text-align: center;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}

.profile-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(79,158,255,0.05) 0%, transparent 60%);
    animation: pulse-glow 4s ease-in-out infinite;
}

@keyframes pulse-glow {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.05); }
}

.profile-photo {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid var(--accent);
    box-shadow: 0 0 20px var(--glow), 0 0 40px rgba(79,158,255,0.1);
    margin-bottom: 12px;
    display: block;
    margin-left: auto;
    margin-right: auto;
}

.profile-name {
    font-family: 'Sora', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-primary) !important;
    margin: 8px 0 4px 0;
}

.profile-title {
    font-size: 0.78rem;
    color: var(--accent) !important;
    font-weight: 500;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
}

.badge {
    display: inline-block;
    background: rgba(79,158,255,0.12);
    border: 1px solid rgba(79,158,255,0.3);
    color: var(--accent) !important;
    font-size: 0.68rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    margin: 2px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.contact-row {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 0;
    font-size: 0.78rem;
    color: var(--text-muted) !important;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.contact-row:last-child { border-bottom: none; }

.contact-icon {
    font-size: 0.9rem;
    width: 20px;
    text-align: center;
}

/* ── Greeting Banner ── */
.greeting-banner {
    background: linear-gradient(135deg, rgba(79,158,255,0.1), rgba(0,229,160,0.05));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 28px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 16px;
    animation: slide-in 0.6s ease-out;
}

@keyframes slide-in {
    from { opacity: 0; transform: translateY(-12px); }
    to { opacity: 1; transform: translateY(0); }
}

.greeting-emoji {
    font-size: 2.5rem;
    animation: wave 2s ease-in-out infinite;
}

@keyframes wave {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(20deg); }
    75% { transform: rotate(-10deg); }
}

.greeting-text h2 {
    font-family: 'Sora', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    margin: 0 0 4px 0;
    color: var(--text-primary) !important;
}

.greeting-text p {
    font-size: 0.88rem;
    color: var(--text-muted) !important;
    margin: 0;
}

/* ── Mode Tabs ── */
.mode-tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 24px;
    flex-wrap: wrap;
}

.mode-tab {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 10px 20px;
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-muted) !important;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
}

.mode-tab.active {
    background: rgba(79,158,255,0.15);
    border-color: var(--accent);
    color: var(--accent) !important;
}

/* ── Chat Messages ── */
.chat-message-user {
    background: rgba(79,158,255,0.1);
    border: 1px solid rgba(79,158,255,0.2);
    border-radius: 16px 16px 4px 16px;
    padding: 14px 18px;
    margin: 8px 0;
    margin-left: 20%;
    font-size: 0.9rem;
    color: var(--text-primary) !important;
    animation: msg-in 0.3s ease-out;
}

.chat-message-bot {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: 16px 16px 16px 4px;
    padding: 14px 18px;
    margin: 8px 0;
    margin-right: 10%;
    font-size: 0.9rem;
    line-height: 1.65;
    color: var(--text-primary) !important;
    animation: msg-in 0.3s ease-out;
}

@keyframes msg-in {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

.bot-label {
    font-size: 0.72rem;
    color: var(--accent) !important;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.user-label {
    font-size: 0.72rem;
    color: var(--text-muted) !important;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
    text-align: right;
}

/* ── Tech Stack Pills ── */
.tech-pill {
    display: inline-block;
    background: rgba(0,229,160,0.08);
    border: 1px solid rgba(0,229,160,0.2);
    color: var(--accent-green) !important;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    margin: 2px;
    letter-spacing: 0.3px;
}

/* ── Section Headers ── */
.section-header {
    font-family: 'Sora', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary) !important;
    margin-bottom: 6px;
}

.section-sub {
    font-size: 0.85rem;
    color: var(--text-muted) !important;
    margin-bottom: 20px;
}

/* ── Result Cards ── */
.result-card {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    margin: 12px 0;
    animation: slide-in 0.4s ease-out;
}

.result-card h4 {
    font-family: 'Sora', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--accent) !important;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

/* ── Score Badge ── */
.score-badge {
    font-family: 'Sora', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    color: var(--accent-green) !important;
    text-align: center;
    padding: 20px;
}

/* ── Input Styling ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 12px 16px !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--glow) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #2E7AE0) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    padding: 12px 28px !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(79,158,255,0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(79,158,255,0.4) !important;
}

/* ── Radio Buttons ── */
.stRadio > div {
    gap: 8px !important;
}

.stRadio > div > label {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 8px 14px !important;
    font-size: 0.85rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
}

.stRadio > div > label:hover {
    border-color: var(--accent) !important;
    background: rgba(79,158,255,0.08) !important;
}

/* ── Divider ── */
hr {
    border-color: var(--border) !important;
    margin: 16px 0 !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: var(--accent) !important;
}

/* ── Voice Button ── */
.voice-btn {
    background: linear-gradient(135deg, rgba(255,107,53,0.2), rgba(255,107,53,0.1));
    border: 1px solid rgba(255,107,53,0.3);
    border-radius: 50%;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    cursor: pointer;
    transition: all 0.2s;
}

/* ── Typing Indicator ── */
.typing-indicator {
    display: flex;
    gap: 4px;
    align-items: center;
    padding: 14px 18px;
}

.typing-dot {
    width: 8px;
    height: 8px;
    background: var(--accent);
    border-radius: 50%;
    animation: typing-bounce 1.2s ease-in-out infinite;
}

.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing-bounce {
    0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
    40% { transform: translateY(-6px); opacity: 1; }
}

/* ── Stats Row ── */
.stat-card {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 16px;
    text-align: center;
}

.stat-number {
    font-family: 'Sora', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--accent) !important;
}

.stat-label {
    font-size: 0.72rem;
    color: var(--text-muted) !important;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }
</style>
""", unsafe_allow_html=True)

# ─── Voice & Greeting JavaScript ────────────────────────────────────────────
st.markdown("""
<script>
function getGreeting() {
    const hour = new Date().getHours();
    if (hour >= 5 && hour < 12) return { text: "Good Morning", emoji: "🌅", sub: "Ready to tackle the day?" };
    if (hour >= 12 && hour < 17) return { text: "Good Afternoon", emoji: "☀️", sub: "Hope your day is going great!" };
    if (hour >= 17 && hour < 21) return { text: "Good Evening", emoji: "🌆", sub: "Winding down or just getting started?" };
    return { text: "Good Night", emoji: "🌙", sub: "Working late? I've got you covered!" };
}

function speakGreeting() {
    const g = getGreeting();
    const msg = new SpeechSynthesisUtterance(
        `${g.text}! I'm Aditya Bambole's digital twin. I'm here to help you learn about Aditya's background, analyze job fit, and prepare for interviews. What would you like to know?`
    );
    msg.rate = 0.9;
    msg.pitch = 1.0;
    msg.volume = 0.8;
    const voices = window.speechSynthesis.getVoices();
    const preferred = voices.find(v => v.name.includes('Google') && v.lang === 'en-US')
                   || voices.find(v => v.lang === 'en-US')
                   || voices[0];
    if (preferred) msg.voice = preferred;
    window.speechSynthesis.speak(msg);
}

function speakText(text) {
    window.speechSynthesis.cancel();
    const clean = text.replace(/[*#_`]/g, '').replace(/\n/g, ' ').substring(0, 500);
    const msg = new SpeechSynthesisUtterance(clean);
    msg.rate = 0.92;
    msg.pitch = 1.0;
    msg.volume = 0.9;
    const voices = window.speechSynthesis.getVoices();
    const preferred = voices.find(v => v.name.includes('Google') && v.lang === 'en-US')
                   || voices.find(v => v.lang === 'en-US')
                   || voices[0];
    if (preferred) msg.voice = preferred;
    window.speechSynthesis.speak(msg);
}

function stopSpeech() {
    window.speechSynthesis.cancel();
}

// Auto-greet on first load
window.addEventListener('load', () => {
    setTimeout(() => {
        if (!sessionStorage.getItem('greeted')) {
            speakGreeting();
            sessionStorage.setItem('greeted', 'true');
        }
    }, 1500);
});
</script>
""", unsafe_allow_html=True)

# ─── Time-based Greeting ─────────────────────────────────────────────────────
def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good Morning", "🌅", "Ready to make today count?"
    elif 12 <= hour < 17:
        return "Good Afternoon", "☀️", "Hope your day is going brilliantly!"
    elif 17 <= hour < 21:
        return "Good Evening", "🌆", "Great time to explore my background!"
    else:
        return "Good Night", "🌙", "Working late? I'm here for you!"

greeting_text, greeting_emoji, greeting_sub = get_greeting()

# ─── Initialize System ───────────────────────────────────────────────────────
@st.cache_resource
def load_system():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="./twin_db", embedding_function=embeddings)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-flash")
    return db, model

def ask_twin(question, db, model):
    docs = db.similarity_search(question, k=4)
    context = "\n".join([d.page_content for d in docs])
    prompt = f"""You are Aditya Bambole's digital twin.
Speak in first person as Aditya. Be professional, warm, confident and specific.
Only use the context provided. Never make up facts.
Keep answers focused and under 200 words unless asked for detail.

Context: {context}

Question: {question}

Answer as Aditya:"""
    response = model.generate_content(prompt)
    return response.text

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="profile-card">
        <img src="https://raw.githubusercontent.com/adityab1402/my-digital-twin/main/Aditya_B.JPG"
             class="profile-photo"
             onerror="this.src='https://img.icons8.com/color/96/user-male-circle--v1.png'"/>
        <div class="profile-name">Aditya Bambole</div>
        <div class="profile-title">Project Management Professional</div>
        <div>
            <span class="badge">PMP</span>
            <span class="badge">Lean Six Sigma</span>
            <span class="badge">Construction</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 0 4px;">
        <div class="contact-row"><span class="contact-icon">📍</span> Houston, TX, USA</div>
        <div class="contact-row"><span class="contact-icon">🎓</span> University of Houston, 2026</div>
        <div class="contact-row"><span class="contact-icon">📧</span> adityabambole14@gmail.com</div>
        <div class="contact-row"><span class="contact-icon">📞</span> +1 713-548-6827</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <a href="https://www.linkedin.com/in/aditya-bambole"
       style="display:block; background:rgba(0,119,181,0.15); border:1px solid rgba(0,119,181,0.3);
              border-radius:10px; padding:8px 14px; text-align:center; color:#0077B5 !important;
              text-decoration:none; font-size:0.82rem; font-weight:600; margin-bottom:8px;">
        🔗 LinkedIn Profile
    </a>
    <a href="https://github.com/adityab1402" target="_blank"
       style="display:block; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1);
              border-radius:10px; padding:8px 14px; text-align:center; color:#E0E0E0 !important;
              text-decoration:none; font-size:0.82rem; font-weight:600; margin-bottom:16px;">
        💻 GitHub Profile
    </a>
    """, unsafe_allow_html=True)

    st.divider()

    mode = st.radio(
        "**Navigation**",
        ["💬 Chat with Me", "💼 Job Fit Analyzer", "🎯 Interview Coach", "ℹ️ About This Project"],
        label_visibility="visible"
    )

    st.divider()

    st.markdown("""
    <div style="text-align:center; padding: 8px 0;">
        <div style="font-size:0.7rem; color:#8892A4; margin-bottom:8px; font-weight:600; letter-spacing:1px; text-transform:uppercase;">Built With</div>
    </div>
    """, unsafe_allow_html=True)

    tech_items = ["LangChain", "Gemini AI", "ChromaDB", "Streamlit", "RAG Pipeline"]
    cols = st.columns(2)
    for i, tech in enumerate(tech_items):
        with cols[i % 2]:
            st.markdown(f'<span class="tech-pill">{tech}</span>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Voice controls
    st.markdown("**🔊 Voice Controls**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👋 Greet Me", use_container_width=True):
            st.markdown("<script>speakGreeting();</script>", unsafe_allow_html=True)
    with col2:
        if st.button("🔇 Stop", use_container_width=True):
            st.markdown("<script>stopSpeech();</script>", unsafe_allow_html=True)

# ─── Load System ─────────────────────────────────────────────────────────────
try:
    db, model = load_system()
    system_ready = True
except Exception as e:
    system_ready = False
    st.error(f"⚠️ System loading error: {str(e)}")

# ─── Main Content ─────────────────────────────────────────────────────────────

# Greeting Banner
st.markdown(f"""
<div class="greeting-banner">
    <div class="greeting-emoji">{greeting_emoji}</div>
    <div class="greeting-text">
        <h2>{greeting_text}! I'm Aditya's Digital Twin 🤖</h2>
        <p>{greeting_sub} — Ask me anything about Aditya's background, skills, or experience!</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Stats Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""<div class="stat-card">
        <div class="stat-number">6+</div>
        <div class="stat-label">Years Experience</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="stat-card">
        <div class="stat-number">6</div>
        <div class="stat-label">Certifications</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="stat-card">
        <div class="stat-number">4</div>
        <div class="stat-label">Industries</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown("""<div class="stat-card">
        <div class="stat-number">PMP</div>
        <div class="stat-label">Certified</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── MODE: CHAT ───────────────────────────────────────────────────────────────
if mode == "💬 Chat with Me":
    st.markdown('<div class="section-header">💬 Chat with Aditya\'s Twin</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Ask me anything — background, skills, experience, goals, or just say hello!</div>', unsafe_allow_html=True)

    # Suggested questions
    st.markdown("**Quick Questions:**")
    q_col1, q_col2, q_col3 = st.columns(3)
    suggested_q = None
    with q_col1:
        if st.button("👋 Tell me about yourself", use_container_width=True):
            suggested_q = "Give me a complete professional introduction about Aditya including his education, work experience, certifications, and career goal"
    with q_col2:
        if st.button("🏗️ Construction experience?", use_container_width=True):
            suggested_q = "Tell me about your construction project management experience"
    with q_col3:
        if st.button("🏆 Top skills?", use_container_width=True):
            suggested_q = "What are your top project management skills?"

    st.markdown("<br>", unsafe_allow_html=True)

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Welcome message
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"{greeting_text}! I'm Aditya Bambole's digital twin — an AI version of him powered by his real personal data. I can answer questions about his background, skills, construction experience, and career goals. What would you like to know? 😊"
        })

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-message-user">
                <div class="user-label">You</div>
                {msg["content"]}
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message-bot">
                <div class="bot-label">🤖 Aditya's Twin</div>
                {msg["content"]}
            </div>""", unsafe_allow_html=True)

    # Handle suggested question
    if suggested_q and system_ready:
        st.session_state.messages.append({"role": "user", "content": suggested_q})
        with st.spinner(""):
            st.markdown("""<div class="chat-message-bot">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>""", unsafe_allow_html=True)
            response = ask_twin(suggested_q, db, model)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.markdown(f"<script>speakText(`{response[:300]}`);</script>", unsafe_allow_html=True)
        st.rerun()

    # Chat input
    user_input = st.chat_input("Ask Aditya anything...")
    if user_input and system_ready:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Aditya's twin is thinking..."):
            response = ask_twin(user_input, db, model)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.markdown(f"<script>speakText(`{response[:300]}`);</script>", unsafe_allow_html=True)
        st.rerun()

# ─── MODE: JOB FIT ────────────────────────────────────────────────────────────
elif mode == "💼 Job Fit Analyzer":
    st.markdown('<div class="section-header">💼 Job Fit Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Paste any job description and instantly see how well Aditya matches the role!</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        jd = st.text_area(
            "Paste Job Description Here:",
            height=250,
            placeholder="Copy and paste the full job description from LinkedIn, Indeed, or any job board..."
        )

        col_a, col_b = st.columns(2)
        with col_a:
            company = st.text_input("Company Name:", placeholder="e.g. Turner Construction")
        with col_b:
            role = st.text_input("Role Title:", placeholder="e.g. Project Manager")

        analyze_btn = st.button("🔍 Analyze My Fit", use_container_width=True)

    with col2:
        st.markdown("""
        <div class="result-card">
            <h4>What You'll Get</h4>
            <p style="font-size:0.85rem; color:#8892A4; line-height:1.7;">
            ✅ Match score (0–100%)<br>
            ✅ Matching skills identified<br>
            ✅ Skill gaps highlighted<br>
            ✅ How to position yourself<br>
            ✅ 3 custom resume bullets<br>
            ✅ Interview talking points
            </p>
        </div>
        """, unsafe_allow_html=True)

    if analyze_btn and jd and system_ready:
        with st.spinner("Analyzing job fit..."):
            prompt = f"""Analyze how well Aditya Bambole fits this job at {company} for the role of {role}.

Job Description: {jd}

Provide a detailed analysis with:
1. MATCH SCORE: Give a percentage (0-100%)
2. MATCHING SKILLS: List what Aditya has that matches
3. SKILL GAPS: What is required that Aditya may lack
4. HOW TO POSITION: How Aditya should present himself for this role
5. TOP 3 RESUME BULLETS: Customized bullet points for this specific job
6. KEY INTERVIEW TALKING POINTS: 2-3 things Aditya should emphasize

Be specific and honest. Use Aditya's real experience."""
            result = ask_twin(prompt, db, model)

        st.markdown("---")
        st.markdown("### 📊 Analysis Results")
        st.markdown(f"""<div class="result-card">
            <h4>Job Fit Analysis — {role} at {company}</h4>
            <p style="font-size:0.88rem; line-height:1.8; white-space:pre-wrap;">{result}</p>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"<script>speakText('Job analysis complete! {result[:200]}');</script>", unsafe_allow_html=True)
    elif analyze_btn and not jd:
        st.warning("Please paste a job description first!")

# ─── MODE: INTERVIEW COACH ────────────────────────────────────────────────────
elif mode == "🎯 Interview Coach":
    st.markdown('<div class="section-header">🎯 Interview Coach</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Practice with AI-generated STAR format answers for any interview question!</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        question = st.text_area(
            "Enter Interview Question:",
            height=100,
            placeholder="e.g. Tell me about a time you managed a difficult project..."
        )

        col_a, col_b = st.columns(2)
        with col_a:
            int_role = st.text_input("Role:", value="Construction Project Manager")
        with col_b:
            int_company = st.text_input("Company:", placeholder="Optional")

        generate_btn = st.button("🎯 Generate STAR Answer", use_container_width=True)

    with col2:
        st.markdown("""
        <div class="result-card">
            <h4>Common Questions to Try</h4>
            <p style="font-size:0.82rem; color:#8892A4; line-height:1.9;">
            • Tell me about yourself<br>
            • Why should we hire you?<br>
            • Tell me about a failure<br>
            • How do you handle pressure?<br>
            • Where do you see yourself in 5 years?<br>
            • What is your greatest strength?
            </p>
        </div>
        """, unsafe_allow_html=True)

    if generate_btn and question and system_ready:
        with st.spinner("Preparing your perfect answer..."):
            prompt = f"""Generate a perfect STAR format interview answer for Aditya Bambole.

Role: {int_role} {f'at {int_company}' if int_company else ''}
Question: {question}

Requirements:
- Use STAR format clearly labeled
- Use ONLY real examples from Aditya's actual experience
- Speak in first person as Aditya
- Be confident and specific with real numbers where possible
- End with a forward-looking statement connecting to this role
- Include a FINAL SPOKEN VERSION that flows naturally"""
            result = ask_twin(prompt, db, model)

        st.markdown("---")
        st.markdown(f"""<div class="result-card">
            <h4>Your STAR Answer</h4>
            <p style="font-size:0.88rem; line-height:1.8; white-space:pre-wrap;">{result}</p>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"<script>speakText(`{result[:400]}`);</script>", unsafe_allow_html=True)

        st.info("💡 Read this answer out loud 3 times. Edit any part that doesn't sound like you. Then practice without looking at it!")
    elif generate_btn and not question:
        st.warning("Please enter an interview question first!")

# ─── MODE: ABOUT ──────────────────────────────────────────────────────────────
elif mode == "ℹ️ About This Project":
    st.markdown('<div class="section-header">ℹ️ About This Project</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">How Aditya built his AI digital twin in 7 days with no prior coding experience</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="result-card">
            <h4>🧠 How It Works</h4>
            <p style="font-size:0.85rem; color:#B0B8C8; line-height:1.8;">
            This digital twin uses <strong style="color:#4F9EFF;">RAG (Retrieval-Augmented Generation)</strong> —
            a technique where personal documents are stored in a vector database.
            When you ask a question, the system finds the most relevant chunks
            of Aditya's data and passes them to Google Gemini AI, which generates
            an answer in Aditya's voice using only real facts.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="result-card">
            <h4>📚 Tech Stack</h4>
            <p style="font-size:0.85rem; color:#B0B8C8; line-height:1.8;">
            <strong style="color:#4F9EFF;">AI Orchestration:</strong> LangChain<br>
            <strong style="color:#4F9EFF;">Language Model:</strong> Google Gemini 2.5 Flash<br>
            <strong style="color:#4F9EFF;">Embeddings:</strong> all-MiniLM-L6-v2 (Free)<br>
            <strong style="color:#4F9EFF;">Vector Database:</strong> ChromaDB<br>
            <strong style="color:#4F9EFF;">Frontend:</strong> Streamlit<br>
            <strong style="color:#4F9EFF;">Hosting:</strong> Streamlit Community Cloud (Free)<br>
            <strong style="color:#4F9EFF;">Voice:</strong> Web Speech API (Browser Built-in)
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="result-card">
            <h4>🚀 What Aditya Learned</h4>
            <p style="font-size:0.85rem; color:#B0B8C8; line-height:1.9;">
            ✅ How RAG architecture works in practice<br>
            ✅ How vector embeddings enable semantic search<br>
            ✅ How to orchestrate LLM pipelines with LangChain<br>
            ✅ How to deploy AI apps with zero cost infrastructure<br>
            ✅ That data quality matters more than model quality<br>
            ✅ How to build a full AI product from scratch in 7 days
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="result-card">
            <h4>📅 Built In 7 Days</h4>
            <p style="font-size:0.85rem; color:#B0B8C8; line-height:1.9;">
            <strong style="color:#4F9EFF;">Day 1:</strong> Self-documentation & account setup<br>
            <strong style="color:#4F9EFF;">Day 2:</strong> Data pipeline & ChromaDB memory<br>
            <strong style="color:#4F9EFF;">Day 3:</strong> RAG chatbot & first conversation<br>
            <strong style="color:#4F9EFF;">Day 4:</strong> Job analyzer & cover letter generator<br>
            <strong style="color:#4F9EFF;">Day 5:</strong> Interview coach & mock interviewer<br>
            <strong style="color:#4F9EFF;">Day 6:</strong> Stunning web app deployment<br>
            <strong style="color:#4F9EFF;">Day 7:</strong> Polish, README & LinkedIn launch
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="result-card" style="text-align:center; margin-top:16px;">
        <h4>💬 Aditya's Message</h4>
        <p style="font-size:0.9rem; color:#B0B8C8; line-height:1.8; font-style:italic; max-width:600px; margin:0 auto;">
        "I come from a project management background, not a technical one.
        But I identified a real problem — the job search process — and built a working AI solution in 7 days.
        This project shows that with curiosity, structure, and determination,
        anyone can build something extraordinary."
        </p>
        <p style="color:#4F9EFF; font-weight:700; margin-top:12px;">— Aditya Bambole</p>
    </div>
    """, unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; padding:16px; border-top:1px solid rgba(79,158,255,0.1);">
    <p style="font-size:0.75rem; color:#8892A4; margin:0;">
        Built by Aditya Bambole with ❤️ using LangChain · Google Gemini · ChromaDB · Streamlit
        &nbsp;|&nbsp;
        <a href="https://github.com/adityab1402" target="_blank" style="color:#4F9EFF; text-decoration:none;">GitHub</a>
        &nbsp;·&nbsp;
        <a href="https://www.linkedin.com/in/aditya-bambole/" target="_blank" style="color:#4F9EFF; text-decoration:none;">LinkedIn</a>
    </p>
</div>
""", unsafe_allow_html=True)
