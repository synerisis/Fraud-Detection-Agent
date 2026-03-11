# Fraud Detection Agent

A local AI agent that answers natural language questions about fraud risk — no API key required. Ask about any person by name, email, phone number, IP address, or physical address and get an instant risk assessment.

![Python](https://img.shields.io/badge/python-3.11+-blue) ![Streamlit](https://img.shields.io/badge/streamlit-1.35+-red) ![Ollama](https://img.shields.io/badge/ollama-local-green)

---

## How it works

```
You → Streamlit UI → AI Agent (Ollama) → MCP Server → Fraud Database
```

- **Ollama** runs a local LLM (no API key, no data leaves your machine)
- **MCP Server** exposes a database of 50 individuals with fraud risk scores across phone, email, IP, and address channels
- **AI Agent** interprets your question, calls the right tools, and returns a structured risk assessment

---

## Setup

**1. Install Ollama**

Download from [ollama.com](https://ollama.com) and pull a model:

```bash
ollama pull qwen2.5:3b        # recommended — fast and reliable tool use
# or
ollama pull llama3.2          # smaller (~2 GB)
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure model (optional)**

```bash
cp .env.example .env
# Edit .env and set OLLAMA_MODEL=qwen2.5:3b
```

**4. Run**

```bash
streamlit run app.py
```

---

## Usage

Ask anything about a person or identifier:

| Query | What it does |
|---|---|
| `Check Carlos Mendez` | Full risk profile by name |
| `Is alice.harmon@gmail.com safe?` | Lookup by email |
| `Who is using IP 185.220.101.66?` | Lookup by IP address |
| `Run a check on +1-901-555-4848` | Lookup by phone |
| `Who is the highest risk person?` | Database summary |

The agent returns a risk score (1–500), per-channel breakdown, fraud signals, and a recommendation:

| Score | Level | Recommendation |
|---|---|---|
| 1–99 | Low Risk | APPROVE |
| 100–249 | Medium Risk | REVIEW |
| 250–399 | High Risk | DECLINE |
| 400–500 | Critical Risk | ESCALATE |

---

## CLI mode

```bash
python agent.py                              # interactive REPL
python agent.py "Check Carlos Mendez"        # single query
```

---

## Project structure

```
agent_core.py   — agentic loop: Ollama ↔ MCP via OpenAI-compatible API
server.py       — MCP server exposing fraud database tools
app.py          — Streamlit chat UI
agent.py        — CLI entry point
data.py         — 50 dummy people with fraud risk scores
```

---

## Model options

Set `OLLAMA_MODEL` in `.env`:

| Model | Size | Notes |
|---|---|---|
| `qwen2.5:3b` | ~1.9 GB | Recommended — fast, reliable tool use |
| `qwen2.5:7b` | ~4.7 GB | Best accuracy |
| `llama3.2` | ~2 GB | Fast but occasional tool-call quirks |
