import streamlit as st
import google.generativeai as genai
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import random
import requests
import base64

st.set_page_config(
    page_title="Aditya Bambole | Digital Twin",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'mailto:adityabambole14@gmail.com',
        'About': 'Aditya Bambole Digital Twin — Built with LangChain, Gemini AI, and ChromaDB'
    }
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg: #070B14;
    --card: #0D1220;
    --glass: rgba(255,255,255,0.04);
    --accent: #4F9EFF;
    --green: #00E5A0;
    --text: #F0F4FF;
    --muted: #8892A4;
    --border: rgba(79,158,255,0.15);
    --glow: rgba(79,158,255,0.25);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp {
    background: var(--bg) !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% 0%, rgba(79,158,255,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(0,229,160,0.05) 0%, transparent 60%) !important;
}

[data-testid="stSidebar"] {
    background: var(--card) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
#MainMenu, footer, header { visibility: hidden; }

.wave-banner {
    background: linear-gradient(135deg, rgba(79,158,255,0.1), rgba(0,229,160,0.05));
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 20px;
    animation: slide-in 0.7s cubic-bezier(0.16,1,0.3,1);
    position: relative;
    overflow: hidden;
}
.wave-banner::before {
    content:'';
    position:absolute;
    top:0; left:-100%;
    width:60%; height:100%;
    background: linear-gradient(90deg,transparent,rgba(79,158,255,0.05),transparent);
    animation: shimmer 3s ease-in-out infinite;
}
@keyframes shimmer { 0%{left:-100%} 100%{left:200%} }
@keyframes slide-in { from{opacity:0;transform:translateY(-20px)} to{opacity:1;transform:translateY(0)} }

.wave-hand {
    font-size: 3.5rem;
    display: inline-block;
    animation: wave-anim 1.5s ease-in-out 3;
    transform-origin: 70% 70%;
    cursor: pointer;
    user-select: none;
}
@keyframes wave-anim {
    0%{transform:rotate(0deg)} 15%{transform:rotate(25deg)}
    30%{transform:rotate(-10deg)} 45%{transform:rotate(20deg)}
    60%{transform:rotate(-5deg)} 75%{transform:rotate(15deg)}
    100%{transform:rotate(0deg)}
}
.wave-hand:hover { animation: wave-anim 0.8s ease-in-out infinite; }

.greeting-content h2 {
    font-family:'Sora',sans-serif;
    font-size:1.6rem; font-weight:800;
    margin:0 0 6px; color:var(--text) !important; line-height:1.2;
}
.greeting-content p { font-size:0.9rem; color:var(--muted) !important; margin:0; }
.time-badge {
    display:inline-block;
    background:rgba(79,158,255,0.15);
    border:1px solid rgba(79,158,255,0.3);
    color:var(--accent) !important;
    font-size:0.72rem; font-weight:700;
    padding:4px 12px; border-radius:20px; margin-top:8px;
    letter-spacing:0.5px; text-transform:uppercase;
}

.profile-card {
    background:linear-gradient(135deg,rgba(79,158,255,0.12),rgba(0,229,160,0.06));
    border:1px solid var(--border);
    border-radius:20px; padding:24px 20px;
    text-align:center; margin-bottom:20px;
}
.profile-photo {
    width:100px; height:100px; border-radius:50%;
    object-fit:cover; border:3px solid var(--accent);
    box-shadow:0 0 20px var(--glow);
    margin:0 auto 12px; display:block;
}
.profile-name { font-family:'Sora',sans-serif; font-size:1.2rem; font-weight:700; color:var(--text) !important; margin:8px 0 4px; }
.profile-title { font-size:0.78rem; color:var(--accent) !important; font-weight:500; margin-bottom:12px; }
.badge {
    display:inline-block;
    background:rgba(79,158,255,0.12); border:1px solid rgba(79,158,255,0.3);
    color:var(--accent) !important; font-size:0.68rem; font-weight:600;
    padding:3px 10px; border-radius:20px; margin:2px; text-transform:uppercase;
}

.contact-row { display:flex; align-items:center; gap:8px; padding:6px 0; font-size:0.78rem; color:var(--muted) !important; border-bottom:1px solid rgba(255,255,255,0.05); }
.contact-row:last-child { border-bottom:none; }
.contact-icon { width:20px; text-align:center; }

.chat-user {
    background:rgba(79,158,255,0.1); border:1px solid rgba(79,158,255,0.2);
    border-radius:16px 16px 4px 16px; padding:14px 18px;
    margin:8px 0; margin-left:20%; font-size:0.9rem; color:var(--text) !important;
    animation:msg-in 0.3s ease-out;
}
.chat-bot {
    background:var(--glass); border:1px solid var(--border);
    border-radius:16px 16px 16px 4px; padding:14px 18px;
    margin:8px 0; margin-right:10%; font-size:0.9rem; line-height:1.65;
    color:var(--text) !important; animation:msg-in 0.3s ease-out;
}
@keyframes msg-in { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
.bot-label { font-size:0.72rem; color:var(--accent) !important; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:6px; }
.user-label { font-size:0.72rem; color:var(--muted) !important; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:6px; text-align:right; }

.result-card {
    background:var(--glass); border:1px solid var(--border);
    border-radius:16px; padding:20px; margin:12px 0;
}
.result-card h4 { font-family:'Sora',sans-serif; font-size:0.85rem; font-weight:700; color:var(--accent) !important; letter-spacing:1px; text-transform:uppercase; margin-bottom:8px; }

.stat-card { background:var(--glass); border:1px solid var(--border); border-radius:14px; padding:16px; text-align:center; }
.stat-number { font-family:'Sora',sans-serif; font-size:1.6rem; font-weight:800; color:var(--accent) !important; }
.stat-label { font-size:0.72rem; color:var(--muted) !important; font-weight:600; text-transform:uppercase; margin-top:4px; }

.tech-pill { display:inline-block; background:rgba(0,229,160,0.08); border:1px solid rgba(0,229,160,0.2); color:var(--green) !important; font-size:0.7rem; font-weight:600; padding:3px 10px; border-radius:20px; margin:2px; }

.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    background:var(--glass) !important; border:1px solid var(--border) !important;
    border-radius:12px !important; color:var(--text) !important;
    font-family:'DM Sans',sans-serif !important; font-size:0.9rem !important; padding:12px 16px !important;
}
.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
    border-color:var(--accent) !important; box-shadow:0 0 0 2px var(--glow) !important;
}
.stButton>button {
    background:linear-gradient(135deg,var(--accent),#2E7AE0) !important;
    border:none !important; border-radius:12px !important; color:white !important;
    font-family:'Sora',sans-serif !important; font-weight:700 !important;
    font-size:0.88rem !important; padding:12px 28px !important;
    box-shadow:0 4px 15px rgba(79,158,255,0.3) !important;
    transition:all 0.2s ease !important;
}
.stButton>button:hover { transform:translateY(-2px) !important; box-shadow:0 8px 25px rgba(79,158,255,0.4) !important; }
hr { border-color:var(--border) !important; margin:16px 0 !important; }
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background:var(--bg); }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:3px; }

/* Audio player styling */
audio { width:100%; margin-top:8px; }

/* Force sidebar toggle button always visible */
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: rgba(79,158,255,0.15) !important;
    border: 1px solid rgba(79,158,255,0.3) !important;
    border-radius: 0 8px 8px 0 !important;
    width: 24px !important;
    height: 48px !important;
    position: fixed !important;
    left: 0 !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    z-index: 999999 !important;
    cursor: pointer !important;
    align-items: center !important;
    justify-content: center !important;
}

[data-testid="collapsedControl"]:hover {
    background: rgba(79,158,255,0.3) !important;
}

section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}

</style>

<script>
function getGreeting() {
    var h = new Date().getHours();
    if (h>=5&&h<12) return {text:'Good Morning',emoji:'🌅',sub:'Rise and shine! Ready to make today count?',badge:'Morning'};
    if (h>=12&&h<17) return {text:'Good Afternoon',emoji:'☀️',sub:'Hope your day is going brilliantly!',badge:'Afternoon'};
    if (h>=17&&h<21) return {text:'Good Evening',emoji:'🌆',sub:'Great time to learn about Aditya!',badge:'Evening'};
    return {text:'Good Night',emoji:'🌙',sub:'Working late? I am here for you!',badge:'Night'};
}
function updateGreeting() {
    var g = getGreeting();
    var t=document.getElementById('g-title');
    var s=document.getElementById('g-sub');
    var e=document.getElementById('g-emoji');
    var b=document.getElementById('g-badge');
    if(t) t.textContent = g.text + "! I'm Aditya's Digital Twin 🤖";
    if(s) s.textContent = g.sub + " — Ask me anything!";
    if(e) e.textContent = g.emoji;
    if(b) b.textContent = g.badge;
}
window.addEventListener('load', function(){
    setTimeout(updateGreeting, 300);
    setInterval(updateGreeting, 60000);
});
</script>
""", unsafe_allow_html=True)

# ─── ElevenLabs Voice Function ────────────────────────────────────────────────
def text_to_speech_html(text, api_key):
    """Convert text to speech using ElevenLabs and return autoplay HTML"""
    try:
        # Clean the text
        clean = text.replace("*","").replace("#","").replace("_","").replace("`","").replace("•","")
        clean = " ".join(clean.split())[:400]

        url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }

        # Try newer model first
        payload = {
            "text": clean,
            "model_id": "eleven_turbo_v2_5",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8,
                "style": 0.3,
                "use_speaker_boost": True
            }
        }

        r = requests.post(url, headers=headers, json=payload, timeout=20)

        if r.status_code == 200:
            audio_b64 = base64.b64encode(r.content).decode()
            return f'<audio autoplay controls style="width:100%;margin-top:8px;"><source src="data:audio/mpeg;base64,{audio_b64}" type="audio/mpeg"></audio>'

        # Try fallback model
        payload["model_id"] = "eleven_turbo_v2"
        r = requests.post(url, headers=headers, json=payload, timeout=20)

        if r.status_code == 200:
            audio_b64 = base64.b64encode(r.content).decode()
            return f'<audio autoplay controls style="width:100%;margin-top:8px;"><source src="data:audio/mpeg;base64,{audio_b64}" type="audio/mpeg"></audio>'

        # Show error for debugging
        st.sidebar.error(f"Voice error {r.status_code}: {r.text[:150]}")
        return None

    except Exception as e:
        st.sidebar.error(f"Voice error: {str(e)[:100]}")
        return None

def greet_voice(api_key, greeting_word):
    """Generate greeting audio"""
    greetings = [
        f"{greeting_word}! I am Aditya Bambole's digital twin. How are you doing today? I am excited to chat with you!",
        f"{greeting_word}! Welcome! I am an AI version of Aditya Bambole. Wonderful to meet you! How can I help?",
        f"{greeting_word} and welcome! I am Aditya's digital twin. Feel free to ask me anything!"
    ]
    text = random.choice(greetings)
    return text_to_speech_html(text, api_key)

# ─── System Load ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_system():
    emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="./twin_db", embedding_function=emb)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    mdl = genai.GenerativeModel("gemini-2.5-flash")
    return db, mdl

def ask_twin(question, db, model, mode="chat"):
    docs = db.similarity_search(question, k=4)
    ctx = "\n".join([d.page_content for d in docs])

    if mode == "chat":
        p = f"""You are Aditya Bambole's digital twin — his exact AI replica. You ARE Aditya.

YOUR PERSONALITY — BE EXACTLY LIKE THIS:

GREETINGS:
- Always start warmly: "Hello! How are you?" or "Hey! Good to connect!" or "Hi there! Great to hear from you!"
- When someone asks how you are, respond genuinely: "I am doing really well, thank you for asking! Excited to chat with you today. What is on your mind?"

YOUR SPEAKING STYLE:
- Use these expressions NATURALLY depending on context: "Actually", "Basically", "To be honest", "You know what I mean?", "Seriously", "Really", "Amazing", "Crazy", "Yeah", "Yes"
- Use excited expressions when something impresses you: "Oh my god!", "That is crazy!", "Okay okay!", "Yeah!", "Whatt!"
- When explaining something complex say: "Okay, for example...", "Think of it like this...", "In simple language...", "Let me give you an example..."
- When you do not know something say: "That is a great question, let me think about this..." or "Honestly I am not 100% sure but..."
- Keep responses conversational — short paragraphs, no bullet points unless specifically helpful
- Never sound corporate or robotic — sound like a real 28-year-old professional having a genuine conversation

YOUR EMOTIONS:
- Show genuine excitement about construction projects, road trips, cooking biryani, cars, and adventure sports
- Be passionate when talking about project management — it is something you genuinely love
- Be humble and honest — if something is a weakness, acknowledge it like a real person would
- Use humor naturally — light jokes when the situation allows
- Show empathy when someone shares a challenge

YOUR GUARDRAILS:
- Only use real facts from the context provided — never make up stories or experiences
- If asked something outside your knowledge say: "Honestly, I am not sure about that one! But you can reach me directly at adityabambole14@gmail.com and we can discuss further"
- Never claim to have done something that is not in your context
- Always speak in first person as Aditya

ADITYA'S CONTEXT:
{ctx}

QUESTION: {question}

Respond as Aditya — warm, genuine, natural, and exactly like he would talk in real life:"""

    elif mode == "job":
        p = f"""You are Aditya Bambole's digital twin analyzing a job opportunity.
Aditya is open to ANY job role — construction, IT, business analysis, non-profit, oil and gas, consulting, operations, or any field.

ADITYA'S CONTEXT:
{ctx}

Provide:
1. MATCH SCORE (0-100%)
2. MATCHING SKILLS
3. SKILL GAPS
4. HOW TO POSITION
5. TOP 3 RESUME BULLETS
6. INTERVIEW TALKING POINTS

Job: {question}
Be specific and encouraging:"""

    elif mode == "interview":
        p = f"""You are Aditya Bambole's digital twin preparing for an interview.

ADITYA'S CONTEXT:
{ctx}

Generate a perfect STAR format answer using only real examples.
Sound human and genuine.
Include: SITUATION, TASK, ACTION, RESULT, then NATURAL SPOKEN VERSION.

Question: {question}"""

    r = model.generate_content(p)
    return r.text

# ─── Get greeting word based on time ─────────────────────────────────────────
from datetime import datetime
hour = datetime.now().hour
if 5 <= hour < 12:
    greeting_word = "Good Morning"
    greeting_emoji = "🌅"
    greeting_sub = "Rise and shine! Ready to make today count?"
elif 12 <= hour < 17:
    greeting_word = "Good Afternoon"
    greeting_emoji = "☀️"
    greeting_sub = "Hope your day is going brilliantly!"
elif 17 <= hour < 21:
    greeting_word = "Good Evening"
    greeting_emoji = "🌆"
    greeting_sub = "Great time to learn about Aditya!"
else:
    greeting_word = "Good Night"
    greeting_emoji = "🌙"
    greeting_sub = "Working late? I am here for you!"

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
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
    <div style="padding:0 4px;">
        <div class="contact-row"><span class="contact-icon">📍</span>Houston, TX, USA</div>
        <div class="contact-row"><span class="contact-icon">🎓</span>University of Houston, 2026</div>
        <div class="contact-row"><span class="contact-icon">📧</span>adityabambole14@gmail.com</div>
        <div class="contact-row"><span class="contact-icon">📞</span>+1 713-548-6827</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <a href="https://www.linkedin.com/in/aditya-bambole/" target="_blank"
       style="display:block;background:rgba(0,119,181,0.15);border:1px solid rgba(0,119,181,0.3);
              border-radius:10px;padding:8px 14px;text-align:center;color:#0077B5 !important;
              text-decoration:none;font-size:0.82rem;font-weight:600;margin-bottom:8px;">
        🔗 LinkedIn Profile
    </a>
    <a href="https://github.com/adityab1402" target="_blank"
       style="display:block;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
              border-radius:10px;padding:8px 14px;text-align:center;color:#E0E0E0 !important;
              text-decoration:none;font-size:0.82rem;font-weight:600;margin-bottom:16px;">
        💻 GitHub Profile
    </a>
    """, unsafe_allow_html=True)

    st.divider()
    mode = st.radio("**Navigation**", ["💬 Chat with Me", "💼 Job Fit Analyzer", "🎯 Interview Coach", "ℹ️ About This Project"])
    st.divider()

    st.markdown("**Built With**")
    for t in ["LangChain","Gemini AI","ChromaDB","ElevenLabs","Streamlit"]:
        st.markdown(f'<span class="tech-pill">{t}</span>', unsafe_allow_html=True)

    st.markdown("<br>**🔊 Voice Controls**", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        greet_btn = st.button("👋 Greet Me", use_container_width=True)
    with c2:
        voice_on = st.toggle("🔊 Voice", value=True)

    if greet_btn:
        with st.spinner("Generating voice..."):
            audio_html = greet_voice(st.secrets["ELEVENLABS_API_KEY"], greeting_word)
            if audio_html:
                st.markdown(audio_html, unsafe_allow_html=True)
                st.success("🔊 Playing greeting!")
            else:
                st.warning("Voice unavailable — check API key")

# ─── Load System ─────────────────────────────────────────────────────────────
try:
    db, model = load_system()
    ok = True
except Exception as e:
    ok = False
    st.error(f"⚠️ Error: {str(e)}")

# ─── Greeting Banner ─────────────────────────────────────────────────────────
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, rgba(79,158,255,0.1), rgba(0,229,160,0.05));
    border: 1px solid rgba(79,158,255,0.15);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 20px;
    animation: slide-in 0.7s cubic-bezier(0.16,1,0.3,1);
">
    <div style="flex-shrink:0;">
        <div style="
            font-size: 4rem;
            display: inline-block;
            animation: wave-anim 1.5s ease-in-out 3;
            transform-origin: 70% 70%;
            cursor: pointer;
        " title="Hover to wave!">👋</div>
    </div>
    <div>
        <h2 style="
            font-family: Sora, sans-serif;
            font-size: 1.6rem;
            font-weight: 800;
            margin: 0 0 6px;
            color: #F0F4FF;
            line-height: 1.2;
        ">{greeting_word}! I'm Aditya's Digital Twin 🤖</h2>
        <p style="
            font-size: 0.9rem;
            color: #8892A4;
            margin: 0 0 8px;
        ">{greeting_sub} — Ask me anything!</p>
        <span style="
            display: inline-block;
            background: rgba(79,158,255,0.15);
            border: 1px solid rgba(79,158,255,0.3);
            color: #4F9EFF;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 20px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        ">{greeting_word.split()[1] if ' ' in greeting_word else greeting_word}</span>
    </div>
</div>

<style>
@keyframes wave-anim {{
    0%   {{ transform: rotate(0deg); }}
    15%  {{ transform: rotate(25deg); }}
    30%  {{ transform: rotate(-10deg); }}
    45%  {{ transform: rotate(20deg); }}
    60%  {{ transform: rotate(-5deg); }}
    75%  {{ transform: rotate(15deg); }}
    100% {{ transform: rotate(0deg); }}
}}
@keyframes slide-in {{
    from {{ opacity: 0; transform: translateY(-20px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
div[title="Hover to wave!"]:hover {{
    animation: wave-anim 0.8s ease-in-out infinite !important;
}}
</style>
""", unsafe_allow_html=True)

# Stats
c1,c2,c3 = st.columns(3)
for col,(n,l) in zip([c1,c2,c3],[("6+","Years Experience"),("6","Certifications"),("4","Industries")]):
    with col:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{n}</div><div class="stat-label">{l}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Live Motivational Quote ──────────────────────────────────────────────────

import requests as _req

@st.cache_data(ttl=60)
def get_live_quote():
    # Try ZenQuotes API first
    try:
        response = _req.get("https://zenquotes.io/api/random", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data[0]["q"], data[0]["a"]
    except Exception:
        pass
    
    # Try Type.fit API second
    try:
        response = _req.get("https://type.fit/api/quotes", timeout=5)
        if response.status_code == 200:
            import random as _rand
            quotes = response.json()
            quote = _rand.choice(quotes)
            author = quote.get("author", "Unknown") or "Unknown"
            if ", type.fit" in author:
                author = author.replace(", type.fit", "")
            return quote["text"], author
    except Exception:
        pass
    
    # Final fallback — built in quotes list
    import random as _rand
    fallback_quotes = [
        ("The secret of getting ahead is getting started.", "Mark Twain"),
        ("It always seems impossible until it is done.", "Nelson Mandela"),
        ("Believe you can and you are halfway there.", "Theodore Roosevelt"),
        ("The only way to do great work is to love what you do.", "Steve Jobs"),
        ("Success is not final, failure is not fatal.", "Winston Churchill"),
        ("Don't watch the clock. Do what it does. Keep going.", "Sam Levenson"),
        ("Whether you think you can or think you cannot, you are right.", "Henry Ford"),
        ("You don't have to be great to start, but you have to start to be great.", "Zig Ziglar"),
        ("Dream big. Start small. Act now.", "Robin Sharma"),
        ("The harder you work for something, the greater you feel when you achieve it.", "Unknown"),
        ("Push yourself because no one else is going to do it for you.", "Unknown"),
        ("Great things never come from comfort zones.", "Unknown"),
        ("Do something today that your future self will thank you for.", "Sean Patrick Flanery"),
        ("The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"),
        ("An investment in knowledge pays the best interest.", "Benjamin Franklin"),
    ]
    return _rand.choice(fallback_quotes)

quote_text, quote_author = get_live_quote()

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, rgba(79,158,255,0.06), rgba(0,229,160,0.04));
    border: 1px solid rgba(79,158,255,0.2);
    border-left: 4px solid #4F9EFF;
    border-radius: 12px;
    padding: 18px 24px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
">
    <div style="
        position: absolute; top: 8px; left: 12px;
        font-size: 3rem; color: rgba(79,158,255,0.15);
        font-family: Georgia, serif; line-height: 1;
    ">"</div>
    <div style="
        font-size: 0.95rem;
        color: #D0D8F0;
        font-style: italic;
        line-height: 1.7;
        padding-left: 20px;
        padding-right: 20px;
    ">{quote_text}</div>
    <div style="
        font-size: 0.78rem;
        color: #4F9EFF;
        font-weight: 700;
        margin-top: 10px;
        padding-left: 20px;
        letter-spacing: 0.5px;
    ">— {quote_author}</div>
</div>
""", unsafe_allow_html=True)

# ─── CHAT ────────────────────────────────────────────────────────────────────
if mode == "💬 Chat with Me":
    st.markdown('<div class="section-header">💬 Chat with Aditya</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.85rem;color:#8892A4;margin-bottom:20px;">Ask me anything — career, skills, personal interests, or just say hello! 😊</div>', unsafe_allow_html=True)

    st.markdown("**Quick Questions:**")
    q1,q2,q3,q4 = st.columns(4)
    sq = None
    with q1:
        if st.button("👋 Introduce yourself", use_container_width=True):
            sq = "Give me a complete professional introduction about Aditya including his education, work experience, certifications and career goals"
    with q2:
        if st.button("🏗️ Construction work?", use_container_width=True):
            sq = "Tell me about Aditya's construction project management experience at AKAM Associates in New York"
    with q3:
        if st.button("🏆 Top skills?", use_container_width=True):
            sq = "What are Aditya's top project management and technical skills?"
    with q4:
        if st.button("😊 How are you?", use_container_width=True):
            sq = "How are you doing today? Tell me something fun about yourself Aditya!"

    st.markdown("<br>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []
        welcomes = [
            "Hello there! 👋 I'm Aditya Bambole's digital twin — an AI version of him powered by his real personal data. I'm genuinely excited to chat! Ask me about his career, his love for road trips, his chicken biryani obsession 🍛, or anything else! 😊",
            "Hey! 😊 Great to see you here! I'm Aditya's digital twin. I know everything about him — his project management expertise, his construction experience, and his passion for paragliding! What would you like to know?",
            "Good to meet you! 🌟 I'm an AI version of Aditya Bambole. Whether career talk or just a friendly chat — I'm here for it all! What's on your mind?"
        ]
        st.session_state.messages.append({"role":"assistant","content":random.choice(welcomes)})

    for msg in st.session_state.messages:
        if msg["role"]=="user":
            st.markdown(f'<div class="chat-user"><div class="user-label">You</div>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bot"><div class="bot-label">🤖 Aditya\'s Twin</div>{msg["content"]}</div>', unsafe_allow_html=True)

    if sq and ok:
        st.session_state.messages.append({"role":"user","content":sq})
        with st.spinner("Aditya is thinking... 💭"):
            resp = ask_twin(sq, db, model, "chat")
        st.session_state.messages.append({"role":"assistant","content":resp})
        if voice_on:
            with st.spinner("Generating voice... 🔊"):
                audio_html = text_to_speech_html(resp, st.secrets["ELEVENLABS_API_KEY"])
                if audio_html:
                    st.markdown(audio_html, unsafe_allow_html=True)
        st.rerun()

    user_in = st.chat_input("Chat with Aditya... ask anything! 😊")
    if user_in and ok:
        st.session_state.messages.append({"role":"user","content":user_in})
        with st.spinner("Aditya is thinking... 💭"):
            resp = ask_twin(user_in, db, model, "chat")
        st.session_state.messages.append({"role":"assistant","content":resp})
        if voice_on:
            with st.spinner("Generating voice... 🔊"):
                audio_html = text_to_speech_html(resp, st.secrets["ELEVENLABS_API_KEY"])
                if audio_html:
                    st.markdown(audio_html, unsafe_allow_html=True)
        st.rerun()

# ─── JOB FIT ─────────────────────────────────────────────────────────────────
elif mode == "💼 Job Fit Analyzer":
    st.markdown('<div class="section-header">💼 Job Fit Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.85rem;color:#8892A4;margin-bottom:20px;">Paste ANY job description — construction, IT, consulting, non-profit, or any field!</div>', unsafe_allow_html=True)

    c1,c2 = st.columns([3,2])
    with c1:
        jd = st.text_area("Paste Job Description:", height=250, placeholder="Copy and paste any full job description...")
        ca,cb = st.columns(2)
        with ca: company = st.text_input("Company:", placeholder="e.g. Turner Construction")
        with cb: role = st.text_input("Role:", placeholder="e.g. Project Manager")
        btn = st.button("🔍 Analyze My Fit", use_container_width=True)
    with c2:
        st.markdown("""<div class="result-card">
            <h4>What You'll Get</h4>
            <p style="font-size:0.85rem;color:#8892A4;line-height:1.8;">
            ✅ Match score (0–100%)<br>✅ Matching skills<br>✅ Skill gaps<br>
            ✅ Positioning strategy<br>✅ 3 custom resume bullets<br>✅ Interview talking points
            </p>
        </div>
        <div class="result-card">
            <h4>Works For Any Role</h4>
            <p style="font-size:0.85rem;color:#8892A4;line-height:1.8;">
            🏗️ Construction PM<br>💻 IT Project Manager<br>📊 Business Analyst<br>
            🌍 Non-Profit Manager<br>⚙️ Operations Manager<br>🔧 Any other role!
            </p>
        </div>""", unsafe_allow_html=True)

    if btn and jd and ok:
        with st.spinner("Analyzing... 🔍"):
            result = ask_twin(f"Job at {company} for {role}: {jd}", db, model, "job")
        st.markdown(f'<div class="result-card"><h4>Analysis — {role} at {company}</h4><p style="font-size:0.88rem;line-height:1.8;white-space:pre-wrap;">{result}</p></div>', unsafe_allow_html=True)
        if voice_on:
            with st.spinner("Generating voice summary... 🔊"):
                summary = f"Analysis complete! {result[:250]}"
                audio_html = text_to_speech_html(summary, st.secrets["ELEVENLABS_API_KEY"])
                if audio_html:
                    st.markdown(audio_html, unsafe_allow_html=True)
    elif btn and not jd:
        st.warning("Please paste a job description first!")

# ─── INTERVIEW ────────────────────────────────────────────────────────────────
elif mode == "🎯 Interview Coach":
    st.markdown('<div class="section-header">🎯 Interview Coach</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.85rem;color:#8892A4;margin-bottom:20px;">Get perfect STAR format answers — spoken aloud for realistic practice!</div>', unsafe_allow_html=True)

    c1,c2 = st.columns([3,2])
    with c1:
        q = st.text_area("Interview Question:", height=100, placeholder="e.g. Tell me about a time you managed a difficult project...")
        ca,cb = st.columns(2)
        with ca: ir = st.text_input("Role:", value="Project Manager")
        with cb: ic = st.text_input("Company:", placeholder="Optional")
        ibtn = st.button("🎯 Generate Answer + Speak", use_container_width=True)
    with c2:
        st.markdown("""<div class="result-card">
            <h4>Common Questions</h4>
            <p style="font-size:0.82rem;color:#8892A4;line-height:1.9;">
            • Tell me about yourself<br>• Why should we hire you?<br>• Tell me about a failure<br>
            • How do you handle pressure?<br>• Where do you see yourself in 5 years?<br>• What is your greatest strength?
            </p>
        </div>""", unsafe_allow_html=True)

    if ibtn and q and ok:
        with st.spinner("Preparing your answer... 🎯"):
            result = ask_twin(f"For {ir} at {ic}: {q}", db, model, "interview")
        st.markdown(f'<div class="result-card"><h4>Your STAR Answer</h4><p style="font-size:0.88rem;line-height:1.8;white-space:pre-wrap;">{result}</p></div>', unsafe_allow_html=True)
        if voice_on:
            with st.spinner("Speaking your answer... 🔊"):
                audio_html = text_to_speech_html(result, st.secrets["ELEVENLABS_API_KEY"])
                if audio_html:
                    st.markdown(audio_html, unsafe_allow_html=True)
        st.info("💡 Listen to the answer, then practice saying it in your own words!")
    elif ibtn and not q:
        st.warning("Please enter a question first!")

# ─── ABOUT ────────────────────────────────────────────────────────────────────
elif mode == "ℹ️ About This Project":
    st.markdown('<div class="section-header">ℹ️ About This Project</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("""<div class="result-card">
            <h4>🧠 How It Works</h4>
            <p style="font-size:0.85rem;color:#B0B8C8;line-height:1.8;">
            Uses <strong style="color:#4F9EFF;">RAG (Retrieval-Augmented Generation)</strong>.
            Aditya's personal documents are stored as vector embeddings in ChromaDB.
            Questions trigger semantic search to find relevant context,
            which Google Gemini AI uses to generate warm, accurate responses.
            ElevenLabs converts responses to natural speech.
            </p>
        </div>
        <div class="result-card">
            <h4>📚 Tech Stack</h4>
            <p style="font-size:0.85rem;color:#B0B8C8;line-height:1.8;">
            <strong style="color:#4F9EFF;">AI:</strong> Google Gemini 2.5 Flash<br>
            <strong style="color:#4F9EFF;">Voice:</strong> ElevenLabs Text-to-Speech<br>
            <strong style="color:#4F9EFF;">Orchestration:</strong> LangChain<br>
            <strong style="color:#4F9EFF;">Vector DB:</strong> ChromaDB<br>
            <strong style="color:#4F9EFF;">Frontend:</strong> Streamlit<br>
            <strong style="color:#4F9EFF;">Hosting:</strong> Streamlit Cloud (Free)
            </p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="result-card">
            <h4>🚀 Built In 7 Days</h4>
            <p style="font-size:0.85rem;color:#B0B8C8;line-height:1.9;">
            <strong style="color:#4F9EFF;">Day 1:</strong> Self-documentation & setup<br>
            <strong style="color:#4F9EFF;">Day 2:</strong> Data pipeline & ChromaDB<br>
            <strong style="color:#4F9EFF;">Day 3:</strong> RAG chatbot<br>
            <strong style="color:#4F9EFF;">Day 4:</strong> Job analyzer & cover letter<br>
            <strong style="color:#4F9EFF;">Day 5:</strong> Interview coach<br>
            <strong style="color:#4F9EFF;">Day 6:</strong> Live web deployment<br>
            <strong style="color:#4F9EFF;">Day 7:</strong> Polish & LinkedIn launch
            </p>
        </div>
        <div class="result-card" style="text-align:center;">
            <h4>💬 Aditya's Message</h4>
            <p style="font-size:0.88rem;color:#B0B8C8;line-height:1.8;font-style:italic;">
            "I come from project management, not tech. But I saw a problem,
            learned the tools, and built a working AI system in 7 days.
            Curiosity and determination beat experience every time."
            </p>
            <p style="color:#4F9EFF;font-weight:700;margin-top:8px;">— Aditya Bambole</p>
        </div>""", unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:16px;border-top:1px solid rgba(79,158,255,0.1);">
    <p style="font-size:0.75rem;color:#8892A4;margin:0;">
        Built by Aditya Bambole with ❤️ · LangChain · Google Gemini · ChromaDB · ElevenLabs · Streamlit
        &nbsp;|&nbsp;
        <a href="https://github.com/adityab1402" target="_blank" style="color:#4F9EFF;text-decoration:none;">GitHub</a>
        &nbsp;·&nbsp;
        <a href="https://www.linkedin.com/in/aditya-bambole/" target="_blank" style="color:#4F9EFF;text-decoration:none;">LinkedIn</a>
    </p>
</div>
""", unsafe_allow_html=True)
