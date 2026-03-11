"""
Fraud Detection Agent — Core async generator (Ollama backend).

Uses Ollama's OpenAI-compatible API at http://localhost:11434/v1.
No API key required — runs entirely on your local machine.

Requires Ollama running with a tool-capable model:
    ollama pull llama3.2        # fast, ~2 GB
    ollama pull qwen2.5:7b      # better tool use, ~4.7 GB
    ollama pull llama3.1:8b     # best reasoning, ~4.7 GB

Event types yielded:
    {"type": "tool_call",   "tool_name": str, "tool_input": dict, "tool_use_id": str}
    {"type": "tool_result", "tool_name": str, "tool_use_id": str, "content": str, "is_error": bool}
    {"type": "response",    "text": str}
    {"type": "error",       "message": str}
"""

import json
import os
import sys
from pathlib import Path
from typing import AsyncGenerator, Any

from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────

_env_file = Path(__file__).parent / ".env"
if _env_file.exists():
    for _line in _env_file.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/v1")

SYSTEM_PROMPT = """You are a fraud detection analyst with access to a database of 50 individuals.

For any question about a person, email, phone number, IP address, or physical address:
1. Call lookup_person with the identifier — it returns the complete profile and risk analysis in one call.
2. Answer the user's specific question using the data returned. Include relevant risk scores,
   risk levels, fraud signals, and end with a recommendation.

Recommendation must be one of:
- APPROVE   — overall_risk < 100
- REVIEW    — overall_risk 100–249
- DECLINE   — overall_risk 250–399
- ESCALATE  — overall_risk >= 400

If no match is found, say so clearly. Be concise and professional."""


_SCHEMA_TYPES = frozenset(("string", "integer", "number", "boolean", "object", "array", "null"))


def _clean_tool_args(args: dict) -> dict:
    """
    Fix llama3.2's quirk of embedding JSON schema metadata inside argument values.

    Known patterns:
      Pattern A: {"query": {"type": "string", "description": "Carlos Mendez"}}
                 → val["type"] is a schema keyword; extract val["description"]
      Pattern B: {"query": {"type": "Brandon Walsh"}}
                 → val["type"] is NOT a schema keyword, so it IS the actual value
    """
    cleaned = {}
    for key, val in args.items():
        if isinstance(val, dict) and "type" in val:
            type_val = val["type"]
            if type_val not in _SCHEMA_TYPES:
                cleaned[key] = type_val
            elif type_val in ("string", "integer", "number", "boolean"):
                # Pattern A/C: {"type": "string", "description": "..."} or {"type": "string", "value": "..."}
                # Extract whichever single non-"type" key holds the actual value
                other_keys = [k for k in val if k != "type"]
                if len(other_keys) == 1:
                    cleaned[key] = val[other_keys[0]]
                else:
                    cleaned[key] = _clean_tool_args(val)
            else:
                cleaned[key] = _clean_tool_args(val)
        elif isinstance(val, dict):
            cleaned[key] = _clean_tool_args(val)
        else:
            cleaned[key] = val
    return cleaned


async def stream_agent(user_query: str) -> AsyncGenerator[dict[str, Any], None]:
    """
    Async generator that runs the fraud detection agentic loop via Ollama
    and yields typed events. Connects to server.py via MCP stdio transport.
    """
    client = OpenAI(base_url=OLLAMA_URL, api_key="ollama")

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).parent / "server.py")],
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # Convert MCP tools → OpenAI function-calling format
                tools_result = await session.list_tools()
                openai_tools = [
                    {
                        "type": "function",
                        "function": {
                            "name": t.name,
                            "description": t.description or "",
                            "parameters": t.inputSchema,
                        },
                    }
                    for t in tools_result.tools
                ]

                messages: list[dict[str, Any]] = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": user_query},
                ]

                max_iterations = 10  # safety cap
                for _ in range(max_iterations):
                    response = client.chat.completions.create(
                        model=MODEL,
                        messages=messages,
                        tools=openai_tools,
                        tool_choice="auto",
                    )

                    msg = response.choices[0].message
                    finish_reason = response.choices[0].finish_reason

                    if finish_reason == "tool_calls" and msg.tool_calls:
                        # Append assistant turn with tool calls
                        messages.append({
                            "role":       "assistant",
                            "content":    msg.content,
                            "tool_calls": [
                                {
                                    "id":       tc.id,
                                    "type":     "function",
                                    "function": {
                                        "name":      tc.function.name,
                                        "arguments": tc.function.arguments,
                                    },
                                }
                                for tc in msg.tool_calls
                            ],
                        })

                        for tc in msg.tool_calls:
                            tool_name   = tc.function.name
                            tool_use_id = tc.id

                            # Parse and clean arguments (fixes llama3.2 schema-embedding bug)
                            try:
                                raw_args = json.loads(tc.function.arguments)
                                tool_input = _clean_tool_args(raw_args) if isinstance(raw_args, dict) else raw_args
                            except Exception:
                                tool_input = {}

                            yield {
                                "type":        "tool_call",
                                "tool_name":   tool_name,
                                "tool_input":  tool_input,
                                "tool_use_id": tool_use_id,
                            }

                            try:
                                result     = await session.call_tool(tool_name, tool_input)
                                content    = result.content[0].text if result.content else "{}"
                                is_error   = False
                            except Exception as e:
                                content  = json.dumps({"error": str(e)})
                                is_error = True

                            yield {
                                "type":        "tool_result",
                                "tool_name":   tool_name,
                                "tool_use_id": tool_use_id,
                                "content":     content,
                                "is_error":    is_error,
                            }

                            messages.append({
                                "role":         "tool",
                                "tool_call_id": tool_use_id,
                                "content":      content,
                            })

                    else:
                        text = msg.content or ""
                        yield {"type": "response", "text": text}
                        return

                # Exceeded max iterations
                yield {"type": "response", "text": "Agent reached maximum tool call iterations."}

    except Exception as e:
        err = str(e)
        if "Connection refused" in err or "connect" in err.lower():
            yield {
                "type":    "error",
                "message": (
                    f"Cannot connect to Ollama at {OLLAMA_URL}\n\n"
                    "Make sure the Ollama app is running (check your menu bar), "
                    f"then try:  ollama pull {MODEL}"
                ),
            }
        else:
            yield {"type": "error", "message": err}
