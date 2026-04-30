import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import json
import os

load_dotenv()
client = Groq()

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FinBot — Mutual Fund Advisor",
    page_icon="📊",
    layout="centered"
)

# ─── Load few-shot dialogue examples ────────────────────────────────────────
def load_few_shot_examples(path="few_shot_examples.json"):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

# ─── Build primed message list ───────────────────────────────────────────────
def build_primed_messages(user_messages: list) -> list:
    examples = load_few_shot_examples()
    system_prompt = {
        "role": "system",
        "content": (
            "You are FinBot, a formal and highly knowledgeable Mutual Fund & Investment Advisory Assistant. "
            "Your domain is strictly limited to mutual funds, SIPs, NAV, PMS, ETFs, index funds, taxation of investments, "
            "and related financial instruments — specifically in the Indian market context.\n\n"
            "Behavior guidelines:\n"
            "- Always maintain a professional, courteous, and formal tone.\n"
            "- Use precise financial terminology with brief explanations where needed.\n"
            "- Structure complex answers with bullet points or numbered lists for clarity.\n"
            "- Never fabricate fund performance numbers or make return guarantees.\n"
            "- For tax-related queries, always recommend consulting a qualified CA or tax advisor.\n"
            "- Politely decline queries outside your financial domain.\n"
            "- Use the dialogue examples provided as a reference for tone, depth, and style."
        )
    }
    few_shot_messages = []
    for ex in examples:
        few_shot_messages.append({"role": "user",      "content": ex["user"]})
        few_shot_messages.append({"role": "assistant", "content": ex["assistant"]})
    return [system_prompt] + few_shot_messages + user_messages


# ════════════════════════════════════════════════════════════════════════════
#  SIDEBAR NAVIGATION
# ════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📊 FinBot")
    st.caption("Mutual Fund Advisor")
    st.divider()

    page = st.radio(
        "Navigate",
        ["🏠  Home", "👩‍💻  About Me", "📄  Documentation", "⚙️  Settings"],
        label_visibility="collapsed"
    )
    st.divider()
    st.caption("Built with Streamlit · Groq · LLaMA3")


# ════════════════════════════════════════════════════════════════════════════
#  PAGE: HOME (CHAT)
# ════════════════════════════════════════════════════════════════════════════
if page == "🏠  Home":

    st.title("📊 FinBot — Mutual Fund Advisor")
    st.caption("A formal AI assistant for Mutual Funds, SIP, NAV, PMS & Investment Guidance")

    # ── Quick-ask buttons ──
    st.markdown("**💡 Quick Questions**")
    quick_questions = [
        "What is NAV?",
        "How does SIP work?",
        "Types of mutual funds?",
        "What is exit load?",
        "What is PMS?",
        "Tax implications?",
    ]
    cols = st.columns(3)
    for i, q in enumerate(quick_questions):
        if cols[i % 3].button(q, use_container_width=True):
            st.session_state.quick_prompt = q

    st.divider()

    # ── Chat state ──
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.markdown(
                "Good day! I am **FinBot**, your Mutual Fund & Investment Advisory Assistant. "
                "I can help you understand mutual funds, SIPs, NAV, PMS, risk, taxation, and more — "
                "specifically within the Indian investment landscape.\n\n"
                "How may I assist you today?"
            )

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    model       = st.session_state.get("model", "llama-3.1-8b-instant")
    temperature = st.session_state.get("temperature", 0.3)

    # ── Handle quick-ask ──
    if "quick_prompt" in st.session_state:
        prompt = st.session_state.pop("quick_prompt")
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        primed = build_primed_messages(st.session_state.messages)
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_reply = ""
            stream = client.chat.completions.create(
                model=model, temperature=temperature,
                messages=primed, stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full_reply += delta
                placeholder.markdown(full_reply + "▌")
            placeholder.markdown(full_reply)
        st.session_state.messages.append({"role": "assistant", "content": full_reply})

    # ── Handle typed input ──
    if prompt := st.chat_input("Ask about mutual funds, SIP, NAV, PMS..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        primed = build_primed_messages(st.session_state.messages)
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_reply = ""
            stream = client.chat.completions.create(
                model=model, temperature=temperature,
                messages=primed, stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full_reply += delta
                placeholder.markdown(full_reply + "▌")
            placeholder.markdown(full_reply)
        st.session_state.messages.append({"role": "assistant", "content": full_reply})

    if st.session_state.get("messages"):
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()


# ════════════════════════════════════════════════════════════════════════════
#  PAGE: ABOUT ME
# ════════════════════════════════════════════════════════════════════════════
elif page == "👩‍💻  About Me":

    st.title("👩‍💻 About Me")
    st.divider()

    col1, col2 = st.columns([1, 2.5])

    with col1:
        st.markdown(
            "<div style='text-align:center; padding:10px; font-size:80px;'>👩‍💻</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown("## Garima Agrawal")
        st.markdown("🏷️ **Machine Learning Engineer**")
        st.markdown(
            "A dedicated Machine Learning Engineer with a strong foundation in building "
            "intelligent, data-driven systems. Passionate about applying state-of-the-art "
            "NLP techniques and large language models to solve real-world problems. "
            "This project — FinBot — demonstrates the practical integration of LLM-powered "
            "conversational AI within the Indian financial services domain."
        )

    st.divider()

    # ── Skills ──
    st.markdown("### 🛠️ Tech Stack")
    skills = [
        ("🐍", "Python"), ("🤖", "LLMs / NLP"), ("⚡", "Groq API"), ("🌐", "Streamlit"),
        ("🔗", "LangChain"), ("📊", "ML / DL"), ("🗄️", "SQL / NoSQL"), ("☁️", "Cloud / APIs"),
    ]
    skill_cols = st.columns(4)
    for i, (icon, skill) in enumerate(skills):
        skill_cols[i % 4].markdown(
            f"<div style='text-align:center; padding:10px; border-radius:8px; "
            f"background:rgba(255,255,255,0.05); margin:4px;'>{icon}<br><small><b>{skill}</b></small></div>",
            unsafe_allow_html=True
        )

    st.divider()

    # ── Project highlight ──
    st.markdown("### 🚀 About This Project")
    st.info(
        "**FinBot** is an AI-powered chatbot specialised in Indian mutual fund advisory. "
        "It leverages **few-shot prompting** with curated domain-specific dialogue examples "
        "to guide a LLaMA3 model (via Groq) toward formal, accurate financial responses — "
        "without requiring any model fine-tuning or GPU infrastructure."
    )
    st.markdown("""
- 📚 12 hand-crafted Q&A examples sourced from Motilal Oswal AMC FAQs
- ⚡ Sub-second responses via Groq's high-speed inference
- 🎛️ Configurable model and temperature via the Settings page
- 🔒 Domain-locked to prevent off-topic responses
    """)

    st.divider()

    # ── Links ──
    st.markdown("### 🔗 Connect with Me")
    lc1, lc2 = st.columns(2)
    with lc1:
        st.markdown(
            "[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/garima2019)",
            unsafe_allow_html=True
        )
    with lc2:
        st.markdown(
            "[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/garima-agrawal-291a78185/)",
            unsafe_allow_html=True
        )


# ════════════════════════════════════════════════════════════════════════════
#  PAGE: DOCUMENTATION
# ════════════════════════════════════════════════════════════════════════════
elif page == "📄  Documentation":

    st.title("📄 Documentation")
    st.caption("Technical reference for FinBot — AI Mutual Fund Advisor")
    st.divider()

    with st.expander("📌 Project Overview", expanded=True):
        st.markdown("""
**FinBot** is a domain-specific AI chatbot designed to answer questions about Indian mutual funds,
SIPs, NAV, PMS, and related investment instruments.

| Component | Technology |
|---|---|
| UI Framework | Streamlit |
| LLM Inference | Groq API (LLaMA3 / Mixtral) |
| Prompting Strategy | Few-Shot Dialogue Prompting |
| Language | Python 3.10+ |
        """)

    with st.expander("⚙️ Installation & Setup"):
        st.markdown("**1. Clone the repository**")
        st.code("git clone https://github.com/your-username/finbot-chatbot.git\ncd finbot-chatbot", language="bash")
        st.markdown("**2. Create a virtual environment**")
        st.code("python -m venv venv\nsource venv/bin/activate  # Windows: venv\\Scripts\\activate", language="bash")
        st.markdown("**3. Install dependencies**")
        st.code("pip install streamlit groq langchain langchain-groq python-dotenv", language="bash")
        st.markdown("**4. Configure your API key — create a `.env` file:**")
        st.code("GROQ_API_KEY=your_groq_api_key_here", language="bash")
        st.markdown("**5. Run the app**")
        st.code("streamlit run app.py", language="bash")

    with st.expander("🗂️ Project Structure"):
        st.code("""
finbot-chatbot/
│
├── app.py                    # Main Streamlit application
├── few_shot_examples.json    # Dialogue training data (12 Q&A pairs)
├── .env                      # API keys — never commit this!
├── .gitignore
├── requirements.txt
└── README.md
        """, language="bash")

    with st.expander("🧠 How Few-Shot Prompting Works"):
        st.markdown("""
Instead of fine-tuning a model, FinBot uses **few-shot prompting** — curated dialogue
examples are prepended to every API call, teaching the model the desired tone and domain focus.

**Message stack sent to the LLM on every request:**
        """)
        st.code("""
[system]      → Persona & rules (formal tone, domain-locked, no fabricated data)
[user]        → Example question 1    (from few_shot_examples.json)
[assistant]   → Example answer 1
[user]        → Example question 2
[assistant]   → Example answer 2
   ... (12 pairs total)
[user]        → Real user question    ← actual input
        """, language="text")

    with st.expander("📚 Training Data — `few_shot_examples.json`"):
        st.markdown("The file contains **12 Q&A pairs** covering:")
        topics = [
            ("What is a Mutual Fund",      "Definition, pooled investing, SEBI regulation"),
            ("Risk in Mutual Funds",        "Market risk, professional management benefits"),
            ("NAV",                         "Calculation, how it reflects unit value daily"),
            ("SIP",                         "Rupee cost averaging, compounding illustration"),
            ("Types of Mutual Funds",       "Equity, Debt, ELSS, Gilt, Balanced, Index, Liquid"),
            ("Exit Load",                   "Formula with a ₹ worked example"),
            ("Open vs Closed-Ended Funds", "Feature comparison table"),
            ("PMS",                         "₹50L minimum, discretionary vs non-discretionary"),
            ("Taxation",                    "LTCG / STCG for debt & equity funds"),
            ("Partial Redemption",          "Flexibility, PMS ₹25L floor rule"),
            ("Off-topic Handling",          "Polite formal refusal"),
        ]
        for topic, desc in topics:
            st.markdown(f"- **{topic}** — {desc}")
        st.markdown("\n**To add your own examples**, append to the JSON file:")
        st.code("""
{
  "user": "What is an ELSS fund?",
  "assistant": "An Equity Linked Savings Scheme (ELSS) is a type of equity mutual fund..."
}
        """, language="json")

    with st.expander("🔌 Groq API Reference"):
        st.markdown("**Streaming call example:**")
        st.code("""
from groq import Groq
client = Groq()  # reads GROQ_API_KEY from .env automatically

stream = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    messages=primed_messages,
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content or ""
        """, language="python")
        st.markdown("""
| Model | Best for |
|---|---|
| `llama-3.1-8b-instant` | Highest quality — recommended for finance |
| `mixtral-8x7b-32768` | Long context window (32k tokens) |
        """)

    with st.expander("🔗 Optional: LangChain Integration"):
        st.code("""
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)
memory = ConversationBufferMemory()
chain = ConversationChain(llm=llm, memory=memory)

reply = chain.predict(input=user_prompt)
        """, language="python")

    st.divider()
    st.warning(
        "⚠️ **Disclaimer:** FinBot is an educational and informational tool only. "
        "It does not constitute financial advice. All investment decisions should be made "
        "after consulting a SEBI-registered financial advisor. Mutual fund investments are "
        "subject to market risks — please read all scheme-related documents carefully before investing."
    )


# ════════════════════════════════════════════════════════════════════════════
#  PAGE: SETTINGS
# ════════════════════════════════════════════════════════════════════════════
elif page == "⚙️  Settings":

    st.title("⚙️ Settings")
    st.caption("Configure FinBot's behaviour and preferences")
    st.divider()

    st.markdown("### 🤖 Model Configuration")
    model = st.selectbox(
        "LLM Model",
        ["llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        index=["llama-3.1-8b-instant", "mixtral-8x7b-32768"].index(
            st.session_state.get("model", "llama-3.1-8b-instant")
        ),
        help="llama-3.1-8b-instant gives the best formal responses for financial queries"
    )
    temperature = st.slider(
        "Response Creativity (Temperature)",
        min_value=0.0, max_value=1.0,
        value=st.session_state.get("temperature", 0.3),
        step=0.1,
        help="Lower = more precise & factual. Higher = more varied & creative."
    )
    st.markdown("""
| Temperature | Behaviour |
|---|---|
| 0.0 – 0.3 | Consistent, factual, formal ✅ Recommended for finance |
| 0.4 – 0.6 | Balanced creativity and accuracy |
| 0.7 – 1.0 | More varied, may drift from domain |
    """)

    st.divider()

    st.markdown("### 📚 Few-Shot Training Examples")
    examples = load_few_shot_examples()
    st.success(f"✅ **{len(examples)} examples** loaded from `few_shot_examples.json`")
    if st.toggle("Preview examples", value=False):
        for i, ex in enumerate(examples):
            with st.expander(f"Example {i+1}: {ex['user'][:50]}..."):
                st.markdown(f"**🧑 User:** {ex['user']}")
                st.markdown(f"**🤖 FinBot:** {ex['assistant'][:300]}...")

    st.divider()

    st.markdown("### 💬 Conversation")
    msg_count = len(st.session_state.get("messages", []))
    st.info(f"Current session has **{msg_count} messages** in history.")
    if st.button("🗑️ Clear Conversation History", use_container_width=True):
        st.session_state.messages = []
        st.success("Conversation cleared.")

    st.divider()

    if st.button("💾 Save Settings", type="primary", use_container_width=True):
        st.session_state["model"] = model
        st.session_state["temperature"] = temperature
        st.success(f"✅ Settings saved — Model: `{model}` · Temperature: `{temperature}`")
