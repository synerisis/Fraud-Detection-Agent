"""
Fraud Detection AI Agent — CLI entry point (Ollama backend).

Connects to the MCP server (server.py) via stdio and uses a local Ollama
model for reasoning. No API key required.

Setup (one-time):
    ollama pull llama3.2          # default model (~2 GB)
    ollama pull qwen2.5:7b        # better tool use (~4.7 GB)

Usage:
    python agent.py
    python agent.py "Is carlos.mendez99@yahoo.com high risk?"
    OLLAMA_MODEL=qwen2.5:7b python agent.py
"""

import asyncio
import sys

from agent_core import MODEL, stream_agent


async def run_agent(user_query: str) -> None:
    """Run one complete agent interaction and print results to the terminal."""
    print(f"\n{'─'*60}")
    print(f"Model : {MODEL}")
    print(f"Query : {user_query}")
    print(f"{'─'*60}")

    async for event in stream_agent(user_query):
        etype = event["type"]

        if etype == "tool_call":
            import json
            print(f"\n[Tool]   {event['tool_name']}({json.dumps(event['tool_input'])})")

        elif etype == "tool_result":
            content = event["content"]
            preview = content[:200] + ("..." if len(content) > 200 else "")
            print(f"[Result] {preview}")

        elif etype == "response":
            print(f"\n{event['text']}")

        elif etype == "error":
            print(f"\n[Error] {event['message']}", file=sys.stderr)


def interactive_mode() -> None:
    """Run an interactive REPL for the fraud detection agent."""
    print("\n" + "="*60)
    print("  FRAUD DETECTION AGENT  (Ollama — no API key required)")
    print(f"  Model: {MODEL}")
    print("="*60)
    print("Enter a name, email, phone, IP, or address to check.")
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            query = input("Query> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            print("Goodbye.")
            break

        asyncio.run(run_agent(query))
        print()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        asyncio.run(run_agent(" ".join(sys.argv[1:])))
    else:
        interactive_mode()
