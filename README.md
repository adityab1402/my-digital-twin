# 🤖 Aditya Bambole — Personal Digital Twin

> **An AI-powered virtual replica of myself, built with LangChain, Google Gemini, ChromaDB, and Streamlit — in 7 days, with no prior coding experience.**

[![Live Demo](https://img.shields.io/badge/🔴_LIVE_DEMO-Try_It_Now-4F9EFF?style=for-the-badge)](https://aditya-bambole-digital-twin.streamlit.app)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Aditya_Bambole-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/aditya-bambole/)
[![GitHub](https://img.shields.io/badge/GitHub-adityab1402-181717?style=for-the-badge&logo=github)](https://github.com/adityab1402)

---

## 🌟 What Is This?

This is a **Personal Digital Twin** — an AI system that replicates my professional identity. It can:

- 💬 **Answer questions about me** in my own voice using my real personal data
- 💼 **Analyze any job description** and tell you how well I match the role
- 🎯 **Coach interview preparation** with STAR-format answers using my real experience
- 🔊 **Speak responses aloud** using ElevenLabs text-to-speech
- 🌍 **Greet users based on their local time** — morning, afternoon, or evening

**Try it right now → [aditya-bambole-digital-twin.streamlit.app](https://aditya-bambole-digital-twin.streamlit.app)**

---

## 🎯 The Problem I Solved

The job search process is time-consuming and repetitive:
- Writing tailored resumes for every application takes hours
- Preparing for interviews requires a coach or practice partner
- Recruiters cannot interact with you 24/7

**My digital twin solves all three — for free, instantly, at scale.**

---

## 🏗️ Architecture

```
Personal Documents          Vector Database         AI Brain
(Resume, Bio, Stories)  →  ChromaDB Embeddings  →  Google Gemini
       ↓                          ↓                      ↓
   TextLoader              Semantic Search          RAG Pipeline
   PyPDFLoader             all-MiniLM-L6-v2        Context + Prompt
                                                         ↓
                                                   Natural Response
                                                   in Aditya's Voice
```

### How RAG Works (Simple Explanation)

1. **Load** — My personal documents (resume, bio, stories) are loaded into the system
2. **Split** — Documents are cut into 500-token chunks with 50-token overlap
3. **Embed** — Each chunk is converted into a 384-dimensional vector using `all-MiniLM-L6-v2`
4. **Store** — Vectors stored in ChromaDB — a searchable semantic database
5. **Retrieve** — Your question is embedded and the top 4 most similar chunks are found
6. **Generate** — Chunks + your question are sent to Google Gemini, which answers in my voice

---

## ✨ Features

| Feature | Description |
|---|---|
| 💬 **Chat Mode** | Ask anything about my background, skills, or life — I answer as myself |
| 💼 **Job Fit Analyzer** | Paste any job description — get match score, skill gaps, resume bullets |
| 🎯 **Interview Coach** | Generate STAR-format answers for any interview question |
| 🔊 **Voice Responses** | ElevenLabs AI voice speaks every response aloud |
| 🌍 **Auto Timezone** | Greeting adjusts to your local time automatically |
| 👋 **Wave Animation** | Animated greeting banner on every visit |
| 📱 **Mobile Friendly** | Works on iPhone, Android, and all browsers |
| 🌐 **Public URL** | Share with anyone — no login required |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **LLM** | Google Gemini 2.5 Flash | Generates responses in my voice |
| **Orchestration** | LangChain | Manages the RAG pipeline |
| **Embeddings** | all-MiniLM-L6-v2 (HuggingFace) | Converts text to searchable vectors |
| **Vector Database** | ChromaDB | Stores and searches my personal data |
| **Voice** | ElevenLabs API | Text-to-speech responses |
| **Frontend** | Streamlit | Web interface |
| **Hosting** | Streamlit Community Cloud | Free public deployment |
| **Version Control** | GitHub | Code storage and CI/CD |

---

## 📁 Project Structure

```
my-digital-twin/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── Aditya_B.JPG          # Profile photo
├── twin_db/              # ChromaDB vector database
│   ├── chroma.sqlite3    # Vector store
│   └── [collection]/     # Embedded chunks
│
└── README.md             # This file
```

---

## 🚀 Run It Locally

### Prerequisites
- Python 3.11+
- Google Gemini API key (free at aistudio.google.com)
- ElevenLabs API key (free tier at elevenlabs.io)

### Setup

```bash
# Clone the repository
git clone https://github.com/adityab1402/my-digital-twin.git
cd my-digital-twin

# Install dependencies
pip install -r requirements.txt

# Create secrets file
mkdir .streamlit
echo 'GEMINI_API_KEY = "your_key_here"' > .streamlit/secrets.toml
echo 'ELEVENLABS_API_KEY = "your_key_here"' >> .streamlit/secrets.toml

# Run the app
streamlit run app.py
```

---

## 📊 What I Learned

Building this project taught me things that years of reading could not:

- **RAG Architecture** — How retrieval-augmented generation works in practice, and why it outperforms fine-tuning for personal knowledge bases
- **Vector Embeddings** — How text is converted into mathematical vectors that enable semantic search
- **LLM Orchestration** — How to build multi-step AI pipelines using LangChain
- **Prompt Engineering** — How the quality of prompts directly determines the quality of AI responses
- **Zero-Cost Deployment** — How to deploy production-grade AI apps with no infrastructure cost
- **Data Quality** — That the AI's output quality is 100% determined by the quality of input data

---

## 🗓️ Built In 7 Days

| Day | What I Built |
|---|---|
| Day 1 | Self-documentation, account setup, personal data collection |
| Day 2 | Data pipeline — loaded documents into ChromaDB vector database |
| Day 3 | RAG chatbot — my twin spoke for the first time |
| Day 4 | Job fit analyzer, resume tailor, cover letter generator |
| Day 5 | Interview simulator — two-mode practice system |
| Day 6 | Stunning web app — deployed live with voice |
| Day 7 | README, LinkedIn launch, recruiter pitch preparation |

---

## 💡 My Background

I am **Aditya Bambole** — a Project Management professional with 6+ years of experience across construction, IT, event management, and non-profit sectors. I recently completed my **Masters in Technology Project Management** from the University of Houston (May 2026).

I am **not** a software engineer. I built this project because I saw a real problem in my job search process and decided to solve it — learning the tools as I went.

**This project demonstrates:**
- Ability to learn new technical domains rapidly
- Product thinking — solving a real problem end-to-end
- Project management discipline — delivered in exactly 7 days
- Comfort working with AI tools that are reshaping every industry

---

## 🔮 Future Roadmap

- [ ] Voice cloning — make the twin sound exactly like me using ElevenLabs
- [ ] Talking avatar — lip-synced video responses using D-ID or HeyGen
- [ ] Long-term memory — remember conversations across sessions
- [ ] Job search automation — auto-apply to matching roles
- [ ] Multi-language support — respond in Hindi, Marathi, and other languages
- [ ] Mobile app — native iOS and Android versions

---

## 📬 Contact

**Aditya Bambole**
- 📧 adityabambole14@gmail.com
- 📞 +1 713-548-6827
- 🔗 [LinkedIn](https://www.linkedin.com/in/aditya-bambole/)
- 💻 [GitHub](https://github.com/adityab1402)
- 🌐 [Digital Twin](https://aditya-bambole-digital-twin.streamlit.app)

---

<div align="center">
  <p>Built with ❤️ by Aditya Bambole</p>
  <p>LangChain · Google Gemini · ChromaDB · ElevenLabs · Streamlit</p>
</div>
