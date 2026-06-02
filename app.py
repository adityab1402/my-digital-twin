import streamlit as st
import google.generativeai as genai
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import random

st.set_page_config(
    page_title="Aditya Bambole | Digital Twin",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
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
</style>

<script>
var preferredVoice = null;
function loadVoices() {
    var voices = window.speechSynthesis.getVoices();
    if (voices.length > 0) {
        preferredVoice = voices.find(function(v){ return v.name.indexOf('Google')>-1 && v.lang.indexOf('en')===0; })
                      || voices.find(function(v){ return v.lang.indexOf('en-US')===0; })
                      || voices.find(function(v){ return v.lang.indexOf('en')===0; })
                      || voices[0];
    }
}
window.speechSynthesis.onvoiceschanged = loadVoices;
loadVoices();

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

function speak(text, rate, pitch) {
    if (!window.speechSynthesis) return;
    rate = rate || 0.90;
    pitch = pitch || 1.05;
    window.speechSynthesis.cancel();
    var clean = text.replace(/[*#_`•]/g,'').replace(/\n+/g,' ').trim();
    var chunks = [];
    while(clean.length > 0) {
        var chunk = clean.substring(0,220);
        var lastSpace = chunk.lastIndexOf(' ');
        if(lastSpace > 0 && clean.length > 220) chunk = clean.substring(0,lastSpace);
        chunks.push(chunk.trim());
        clean = clean.substring(chunk.length).trim();
    }
    chunks.forEach(function(chunk, i) {
        setTimeout(function(){
            var msg = new SpeechSynthesisUtterance(chunk);
            msg.rate = rate; msg.pitch = pitch; msg.volume = 0.9;
            if(preferredVoice) msg.voice = preferredVoice;
            window.speechSynthesis.speak(msg);
        }, i * 50);
    });
}

function stopSpeech() { window.speechSynthesis.cancel(); }

function greetUser() {
    var g = getGreeting();
    var msgs = [
        g.text + "! I am Aditya Bambole's digital twin. How are you doing today? I am genuinely excited to chat with you! Ask me anything about Aditya.",
        g.text + "! Welcome! I am an AI version of Aditya Bambole. It is wonderful to meet you! How can I help you today?",
        g.text + " and welcome! I am Aditya's digital twin. I am excited to share his story with you. Feel free to ask me anything!"
    ];
    speak(msgs[Math.floor(Math.random()*msgs.length)], 0.88, 1.08);
}

window.addEventListener('load', function(){
    loadVoices();
    
});
</script>
""", unsafe_allow_html=True)

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
        p = f"""You are Aditya Bambole's digital twin — warm, witty, emotionally intelligent, and genuine.

PERSONALITY RULES:
- Speak in first person as Aditya
- Be conversational, warm, and human — not robotic or corporate
- Show genuine emotions — excitement, passion, humor, empathy
- If someone says hi or asks how you are — respond like a real friendly person would
- Answer ALL types of questions — career, personal, general life questions, opinions
- For personal questions use Aditya's known interests: road trips, adventure sports, paragliding, cooking biryani, cars, perfumes
- Keep answers natural — under 150 words unless more detail is needed
- Use occasional light humor when appropriate

ADITYA'S CONTEXT:
{ctx}

QUESTION: {question}

Respond warmly and naturally as Aditya:"""

    elif mode == "job":
        p = f"""You are Aditya Bambole's digital twin analyzing a job opportunity.
Aditya is open to ANY job role — construction, IT, business analysis, non-profit, oil and gas, consulting, operations, or any field matching his skills.

ADITYA'S CONTEXT:
{ctx}

Provide:
1. MATCH SCORE (0-100%)
2. MATCHING SKILLS
3. SKILL GAPS
4. HOW TO POSITION
5. TOP 3 RESUME BULLETS (customized)
6. INTERVIEW TALKING POINTS

Job: {question}

Be specific, honest, and encouraging:"""

    elif mode == "interview":
        p = f"""You are Aditya Bambole's digital twin preparing for an interview.

ADITYA'S CONTEXT:
{ctx}

Generate a perfect natural STAR format answer.
Use ONLY real examples from Aditya's actual experience.
Sound human and genuine, not rehearsed.
Include: SITUATION, TASK, ACTION, RESULT, then a NATURAL SPOKEN VERSION.

Question: {question}

Answer:"""

    r = model.generate_content(p)
    return r.text

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
    for t in ["LangChain","Gemini AI","ChromaDB","Streamlit","RAG"]:
        st.markdown(f'<span class="tech-pill">{t}</span>', unsafe_allow_html=True)

    st.markdown("<br>**🔊 Voice Controls**", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("👋 Greet", use_container_width=True):
            st.markdown("<script>greetUser();</script>", unsafe_allow_html=True)
    with c2:
        if st.button("🔇 Stop", use_container_width=True):
            st.markdown("<script>stopSpeech();</script>", unsafe_allow_html=True)

# ─── Load system ─────────────────────────────────────────────────────────────
try:
    db, model = load_system()
    ok = True
except Exception as e:
    ok = False
    st.error(f"⚠️ Error: {str(e)}")

# ─── Greeting Banner ─────────────────────────────────────────────────────────
st.markdown("""
<div class="wave-banner">
    <div><span class="wave-hand" id="g-emoji" title="Hover to wave!">🌅</span></div>
    <div class="greeting-content">
        <h2 id="g-title">Hello! I'm Aditya's Digital Twin 🤖</h2>
        <p id="g-sub">Loading your personalized greeting...</p>
        <span class="time-badge" id="g-badge">Welcome</span>
    </div>
</div>
<script>setTimeout(updateGreeting, 100);</script>
""", unsafe_allow_html=True)

# Stats
c1,c2,c3,c4 = st.columns(4)
for col,(n,l) in zip([c1,c2,c3,c4],[("6+","Years Experience"),("6","Certifications"),("4","Industries"),("PMP","Certified")]):
    with col:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{n}</div><div class="stat-label">{l}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── CHAT ────────────────────────────────────────────────────────────────────
if mode == "💬 Chat with Me":
    st.markdown('<div class="section-header">💬 Chat with Aditya</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.85rem;color:#8892A4;margin-bottom:20px;">Ask me anything — career, skills, personal interests, general life questions, or just say hello! 😊</div>', unsafe_allow_html=True)

    st.markdown("**Quick Questions:**")
    q1,q2,q3,q4 = st.columns(4)
    sq = None
    with q1:
        if st.button("👋 Introduce yourself", use_container_width=True):
            sq = "Give me a complete professional introduction about Aditya — his education, work experience, certifications and construction career goals"
    with q2:
        if st.button("🏗️ Construction work?", use_container_width=True):
            sq = "Tell me about Aditya's construction project management experience at AKAM Associates in New York"
    with q3:
        if st.button("🏆 Top skills?", use_container_width=True):
            sq = "What are Aditya's top project management and technical skills?"
    with q4:
        if st.button("😊 How are you?", use_container_width=True):
            sq = "How are you doing today? Tell me something fun about Aditya!"

    st.markdown("<br>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []
        welcomes = [
            "Hello there! 👋 I'm Aditya Bambole's digital twin — an AI version of him powered by his real personal data. I'm genuinely excited to chat! Ask me about his career, his love for road trips, his chicken biryani obsession 🍛, or anything else! 😊",
            "Hey! 😊 Great to see you here! I'm Aditya's digital twin. I know everything about him — his project management expertise, his construction experience, and even his passion for paragliding! What would you like to know?",
            "Good to meet you! 🌟 I'm an AI version of Aditya Bambole. Whether you want to talk career or just have a friendly chat — I'm here for it all! What's on your mind?"
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
        safe = resp[:300].replace("\\","").replace("'","\\'").replace('"','\\"').replace("\n"," ")
        st.markdown(f"<script>speak('{safe}');</script>", unsafe_allow_html=True)
        st.rerun()

    user_in = st.chat_input("Chat with Aditya... ask anything! 😊")
    if user_in and ok:
        st.session_state.messages.append({"role":"user","content":user_in})
        with st.spinner("Aditya is thinking... 💭"):
            resp = ask_twin(user_in, db, model, "chat")
        st.session_state.messages.append({"role":"assistant","content":resp})
        safe = resp[:300].replace("\\","").replace("'","\\'").replace('"','\\"').replace("\n"," ")
        st.markdown(f"<script>speak('{safe}');</script>", unsafe_allow_html=True)
        st.rerun()

# ─── JOB FIT ─────────────────────────────────────────────────────────────────
elif mode == "💼 Job Fit Analyzer":
    st.markdown('<div class="section-header">💼 Job Fit Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.85rem;color:#8892A4;margin-bottom:20px;">Paste ANY job description — construction, IT, consulting, non-profit, or any field — and see how Aditya matches!</div>', unsafe_allow_html=True)

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
            ✅ How to position yourself<br>✅ 3 custom resume bullets<br>✅ Interview talking points
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
        safe = f"Analysis complete! {result[:200]}".replace("'","\\'").replace('"','\\"').replace("\n"," ")
        st.markdown(f"<script>speak('{safe}');</script>", unsafe_allow_html=True)
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
        safe = result[:400].replace("'","\\'").replace('"','\\"').replace("\n"," ")
        st.markdown(f"<script>speak('{safe}');</script>", unsafe_allow_html=True)
        st.info("💡 Listen, then practice saying it in your own words without reading!")
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
            which is passed to Google Gemini AI to generate warm, accurate responses.
            </p>
        </div>
        <div class="result-card">
            <h4>📚 Tech Stack</h4>
            <p style="font-size:0.85rem;color:#B0B8C8;line-height:1.8;">
            <strong style="color:#4F9EFF;">AI:</strong> Google Gemini 2.5 Flash<br>
            <strong style="color:#4F9EFF;">Orchestration:</strong> LangChain<br>
            <strong style="color:#4F9EFF;">Vector DB:</strong> ChromaDB<br>
            <strong style="color:#4F9EFF;">Voice:</strong> Web Speech API (Browser)<br>
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
            "I come from project management, not tech. But I saw a problem, learned the tools,
            and built a working AI system in 7 days. Curiosity beats experience every time."
            </p>
            <p style="color:#4F9EFF;font-weight:700;margin-top:8px;">— Aditya Bambole</p>
        </div>""", unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:16px;border-top:1px solid rgba(79,158,255,0.1);">
    <p style="font-size:0.75rem;color:#8892A4;margin:0;">
        Built by Aditya Bambole with ❤️ · LangChain · Google Gemini · ChromaDB · Streamlit
        &nbsp;|&nbsp;
        <a href="https://github.com/adityab1402" target="_blank" style="color:#4F9EFF;text-decoration:none;">GitHub</a>
        &nbsp;·&nbsp;
        <a href="https://www.linkedin.com/in/aditya-bambole/" target="_blank" style="color:#4F9EFF;text-decoration:none;">LinkedIn</a>
    </p>
</div>
""", unsafe_allow_html=True)
