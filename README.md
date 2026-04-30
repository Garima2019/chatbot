# 📊 FinBot — AI-Powered Mutual Fund Advisor Chatbot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Groq-00A67E?style=for-the-badge&logo=groq&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white"/>
  <img src="https://img.shields.io/badge/LLM-LLaMA3-blueviolet?style=for-the-badge"/>
</p>

<p align="center">
  A domain-specific AI chatbot that answers questions about Mutual Funds, SIP, NAV, PMS, and Indian investment instruments — powered by Groq's ultra-fast LLM inference and guided by few-shot dialogue training.
</p>

---

## 🖥️ Demo

> FinBot greets users formally, answers financial queries with structured responses, and politely declines off-topic questions.

```
User   → "What is SIP and why should I consider it?"
FinBot → "A Systematic Investment Plan (SIP) is a disciplined investment method
          wherein you commit a fixed sum at regular intervals into a mutual fund
          scheme of your choice. Key benefits include Rupee Cost Averaging,
          Power of Compounding, and Financial Discipline..."
```

---

## ✨ Features

- 🤖 **Few-Shot Prompted LLM** — 12 domain-specific Q&A examples teach the bot tone, style, and financial accuracy
- 💬 **Streaming Responses** — Word-by-word output with a live typing cursor for better UX
- 📚 **Domain-Locked** — Strictly focused on Indian mutual funds, SIP, NAV, PMS, ETFs, taxation
- 🎛️ **Sidebar Controls** — Switch models, adjust temperature, preview loaded examples
- ⚡ **Quick-Ask Buttons** — One-click common questions (NAV, SIP, exit load, fund types, etc.)
- 🧹 **Session Management** — Clear conversation history anytime
- 🔒 **Formal Tone** — Never fabricates returns; recommends CA/tax advisor for tax queries

---

## 🏗️ Architecture

```
User Input
    │
    ▼
Streamlit UI  ──────────────────────────────────────────────┐
(chat_input / quick-ask buttons)                            │
    │                                                       │
    ▼                                                       │
build_primed_messages()                                     │
    │                                                       │
    ├── [System Prompt]         ← defines persona & rules   │
    ├── [Few-Shot Examples]     ← few_shot_examples.json    │
    └── [Real Conversation]     ← st.session_state.messages │
                                                            │
    ▼                                                       │
Groq API  (LLaMA3 / Mixtral)                               │
    │                                                       │
    ▼                                                       │
Streamed Response  ──────────────────────────────────────── ┘
    │
    ▼
Displayed in Chat UI
```

---

## 🗂️ Project Structure

```
finbot-chatbot/
│
├── app.py                    # Main Streamlit application
├── few_shot_examples.json    # Domain-specific dialogue training data (12 Q&A pairs)
├── .env                      # API keys — never commit this!
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/finbot-chatbot.git
cd finbot-chatbot
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> 🔑 Get your free API key at [console.groq.com](https://console.groq.com)

### 5. Run the app

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 📦 Requirements

```txt
streamlit
groq
langchain
langchain-groq
python-dotenv
```

Install all at once:

```bash
pip install streamlit groq langchain langchain-groq python-dotenv
```

---

## 🧠 How Few-Shot Training Works

Instead of fine-tuning a model (which requires GPUs and thousands of samples), this project uses **few-shot prompting** — a technique where curated dialogue examples are injected into every API call to guide the model's behaviour.

```
┌─────────────────────────────────────────┐
│           Message Stack Sent to LLM     │
├─────────────────────────────────────────┤
│  [system]     Persona + rules           │
│  [user]       Example Q 1               │
│  [assistant]  Example A 1               │
│  [user]       Example Q 2               │
│  [assistant]  Example A 2               │
│       ... (12 examples total)           │
│  [user]       Real user question        │  ← actual input
└─────────────────────────────────────────┘
```

The model sees your examples as prior "memory" — it naturally mirrors the tone, depth, and domain focus you defined.

---

## 📚 Training Data — `few_shot_examples.json`

The file contains 12 hand-crafted Q&A pairs sourced from online, covering:

| Topic | Description |
|---|---|
| What is a Mutual Fund | Definition, how pooled investing works |
| Risk in Mutual Funds | Market risk, professional management |
| NAV | Calculation, how it reflects unit value |
| SIP | Rupee cost averaging, power of compounding |
| Types of Mutual Funds | Equity, Debt, ELSS, Gilt, Balanced, Index, Liquid |
| Exit Load | How it's calculated with a ₹ example |
| Open vs Closed Ended | Feature comparison table |
| PMS | ₹50L minimum, discretionary vs non-discretionary |
| Taxation | LTCG/STCG for debt and equity funds |
| Partial Redemption | Flexibility of partial withdrawals |
| Off-topic Handling | Polite refusal for non-finance queries |

### Adding your own examples

Simply append to `few_shot_examples.json`:

```json
{
  "user": "What is an ELSS fund?",
  "assistant": "An Equity Linked Savings Scheme (ELSS) is a type of equity mutual fund that offers tax deductions of up to ₹1.5 lakhs per annum under Section 80C of the Income Tax Act. It carries a mandatory lock-in period of 3 years — the shortest among all 80C instruments — and invests primarily in equity and equity-related securities, offering potential for capital appreciation alongside tax benefits."
}
```

---

## ⚙️ Configuration

| Setting | Default | Description |
|---|---|---|
| Model | `llama-3.1-8b-instant` | LLM used for inference |
| Temperature | `0.3` | Lower = more factual; Higher = more creative |
| Max tokens | `1000` | Maximum response length |

### Available Models on Groq

| Model | Strength |
|---|---|
| `llama-3.1-8b-instant` | Best quality, recommended for finance |
| `mixtral-8x7b-32768` | Long context (32k tokens) |

---

## 🔧 Optional: LangChain Integration

If you prefer structured memory management, replace the Groq client with LangChain:

```python
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)
memory = ConversationBufferMemory()
chain = ConversationChain(llm=llm, memory=memory)

reply = chain.predict(input=user_prompt)
```

LangChain handles conversation history automatically — no need to manage `session_state.messages` manually.

---

## 🛡️ .gitignore

```gitignore
.env
venv/
__pycache__/
*.pyc
.DS_Store
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add: your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## ⚠️ Disclaimer

FinBot is an **educational and informational tool only**. It does not constitute financial advice. All investment decisions should be made after consulting a SEBI-registered financial advisor. Mutual fund investments are subject to market risks — please read all scheme-related documents carefully before investing.

---

## 📄 License

This project was developed for academic purposes to create chatbot using machine learning techniques.

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) — Ultra-fast LLM inference
- [Streamlit](https://streamlit.io) — Rapid UI development
- [Meta LLaMA 3](https://llama.meta.com) — Underlying language model

---

<p align="center">Built with ❤️ using Python · Streamlit · Groq · LLaMA3</p>

