# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Project

**Streamlit UI (primary):**
```bash
streamlit run app.py
```

**CLI mode:**
```bash
python agent.py                              # interactive REPL
python agent.py "Check Carlos Mendez"        # single query
OLLAMA_MODEL=qwen2.5:7b python agent.py      # use a different model
```

**Sample queries (batch):**
```bash
./run_samples.sh
```

**Prerequisites:** Ollama must be running (open the Ollama menu bar app). Pull a model first:
```bash
ollama pull llama3.2      # default (~2 GB)
ollama pull qwen2.5:7b    # better tool use (~4.7 GB)
```

## Architecture

Three-layer architecture:

```
app.py / agent.py          ← UI / CLI consumers
      ↓
agent_core.py              ← async generator: stream_agent()
      ↓ stdio subprocess
server.py (MCP server)     ← exposes tools over Model Context Protocol
      ↓
data.py                    ← 50 dummy people with fraud risk scores
```

**`data.py`** — Static list of 50 people (`PEOPLE`), each with `phone_risk`, `email_risk`, `ip_risk`, `address_risk` (0.0–1.0) and `overall_risk` (1–500).

**`server.py`** — FastMCP server run as a subprocess. Tools: `search_person`, `get_person_by_id`, `get_risk_analysis`, `list_high_risk_persons`, `get_database_statistics`. Launched fresh per agent session via stdio.

**`agent_core.py`** — Async generator `stream_agent(user_query)` that:
1. Connects to Ollama via OpenAI-compatible API (`http://localhost:11434/v1`)
2. Spawns `server.py` as an MCP stdio subprocess
3. Converts MCP tool schemas to OpenAI function-calling format
4. Runs the agentic loop (max 10 iterations) and yields typed event dicts

Events yielded: `tool_call`, `tool_result`, `response`, `error`.

**`app.py`** — Streamlit UI. Key design: `stream_agent()` is async, Streamlit is sync. Bridge: run async generator in a background `threading.Thread` with `asyncio.new_event_loop()`, collect events into a `queue.Queue`, then render all at once after completion.

## Key Implementation Details

**llama3.2 tool arg bug:** llama3.2 sometimes embeds JSON schema metadata inside argument values — `{"query": {"description": "Carlos Mendez", "type": "string"}}` instead of `{"query": "Carlos Mendez"}`. Fixed in `agent_core._clean_tool_args()` which detects dicts with both `"type"` and `"description"` keys where type is a JSON primitive, and extracts the `"description"` value.

**Model config:** Set via `OLLAMA_MODEL` env var or `.env` file (`OLLAMA_MODEL=qwen2.5:7b`). Defaults to `llama3.2`. `qwen2.5:7b` has more reliable tool use.

**Risk score ranges:** Individual channels: 0.0–0.29 Low, 0.30–0.59 Medium, 0.60–1.0 High. Overall: 1–99 Low, 100–249 Medium, 250–399 High, 400–500 Critical.

**Sidebar stats** are computed directly from `data.PEOPLE` (no agent call) for instant load.
