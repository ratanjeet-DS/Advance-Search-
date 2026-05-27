# 📈 Zerodha Ecosystem AI Agent

An AI-powered chatbot that searches Zerodha Support, Varsity, Z-Connect,
and TradingQnA to answer your questions — with full conversation memory.

Built with: **Google Gemini 2.5 Flash · LangGraph · LangChain · Streamlit**

---

## 🚀 Setup (Step by Step)

### Step 1 — Prerequisites
Make sure you have **Python 3.10 or higher** installed.
Check with: `python --version`

---

### Step 2 — Open the Project in VS Code
```
File → Open Folder → select the `zerodha_agent` folder
```

---

### Step 3 — Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

---

### Step 4 — Install All Dependencies
```bash
pip install -r requirements.txt
```
This installs Streamlit, LangChain, LangGraph, Gemini SDK, and more.

---

### Step 5 — Get a Free Google Gemini API Key
1. Go to https://aistudio.google.com/app/apikey
2. Click **"Create API Key"**
3. Copy the key — you'll paste it into the app sidebar

---

### Step 6 — Run the App
```bash
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501`

---

## 💬 How to Use

1. Paste your Gemini API Key in the **left sidebar**
2. Type your question in the chat box at the bottom
3. The agent will search Zerodha's ecosystem and reply
4. Ask follow-up questions — it remembers the conversation!
5. Click **"Clear Conversation"** in the sidebar to start fresh

### Example Questions
- *"What are the equity delivery brokerage charges?"*
- *"How do I add a nominee to my Zerodha account?"*
- *"Explain the concept of option Greeks from Varsity"*
- *"What is the margin requirement for overnight F&O positions?"*

---

## 📁 Project Structure

```
zerodha_agent/
├── app.py              ← Main application (all the code lives here)
├── requirements.txt    ← All Python dependencies
├── .env.example        ← Optional: store your API key as env variable
└── README.md           ← This file
```

---

## 🛠 Troubleshooting

| Problem | Fix |
|---|---|
| Pylance import warnings in VS Code | Select the `venv` interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter" → pick `venv` |
| `ModuleNotFoundError` on run | Make sure venv is activated and `pip install -r requirements.txt` was run inside it |
| Invalid API Key error | Double-check the key at https://aistudio.google.com/app/apikey |
| Quota exceeded error | You've hit Gemini's free tier limit — wait or upgrade your plan |
| DuckDuckGo search fails | DuckDuckGo occasionally rate-limits — wait a minute and try again |
