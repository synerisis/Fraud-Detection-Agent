"""
Fraud Detection Agent — Streamlit UI

Run with:
    streamlit run app.py
"""

import asyncio
import json
import queue
import threading

import streamlit as st

import agent_core
from agent_core import stream_agent
from data import PEOPLE

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="Fraud Detection Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# RISK COLOURS
# ──────────────────────────────────────────────

RISK_STYLE: dict[str, dict[str, str]] = {
    "Low":           {"bg": "#d4edda", "fg": "#155724", "border": "#c3e6cb"},
    "Medium":        {"bg": "#fff3cd", "fg": "#856404", "border": "#ffeeba"},
    "High":          {"bg": "#ffe0b2", "fg": "#e65100", "border": "#ffcc80"},
    "Low Risk":      {"bg": "#d4edda", "fg": "#155724", "border": "#c3e6cb"},
    "Medium Risk":   {"bg": "#fff3cd", "fg": "#856404", "border": "#ffeeba"},
    "High Risk":     {"bg": "#ffe0b2", "fg": "#e65100", "border": "#ffcc80"},
    "Critical Risk": {"bg": "#f8d7da", "fg": "#721c24", "border": "#f5c6cb"},
}
_DEFAULT_STYLE = RISK_STYLE["Medium"]


def _badge(label: str) -> str:
    c = RISK_STYLE.get(label, _DEFAULT_STYLE)
    return (
        f'<span style="background:{c["bg"]};color:{c["fg"]};'
        f'border:1px solid {c["border"]};padding:3px 10px;'
        f'border-radius:12px;font-weight:700;font-size:0.78em">{label}</span>'
    )


def _bar_color(score: float) -> str:
    if score < 0.3:   return "#28a745"
    if score < 0.6:   return "#ffc107"
    if score < 0.8:   return "#fd7e14"
    return "#dc3545"


def _inline_bar(score: float, width: int = 110) -> str:
    pct    = int(score * 100)
    color  = _bar_color(score)
    filled = int(width * score)
    return (
        f'<div style="display:inline-flex;align-items:center;gap:6px">'
        f'<div style="width:{width}px;height:9px;background:#e9ecef;'
        f'border-radius:5px;overflow:hidden">'
        f'<div style="width:{filled}px;height:100%;background:{color}"></div>'
        f'</div>'
        f'<span style="font-size:0.8em;color:#555">{pct}%</span>'
        f'</div>'
    )

# ──────────────────────────────────────────────
# RISK CARD
# ──────────────────────────────────────────────

def render_risk_card(analysis: dict) -> None:
    overall = analysis.get("overall_risk", {})
    score   = overall.get("score", 0)
    level   = overall.get("level", "Unknown")
    name    = analysis.get("name", "Unknown")
    rb      = analysis.get("risk_breakdown", {})
    signals = analysis.get("fraud_signals", [])
    c       = RISK_STYLE.get(level, _DEFAULT_STYLE)

    st.markdown(
        f'<div style="border:1px solid {c["border"]};border-radius:10px;'
        f'padding:16px;margin:8px 0;background:{c["bg"]}20">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">'
        f'<span style="font-size:1.05em;font-weight:700">{name.upper()}</span>'
        f'{_badge(level)}'
        f'</div>'
        f'<div style="font-size:0.85em;color:#555;margin-bottom:4px">'
        f'Overall score: <strong>{score} / 500</strong></div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.progress(score / 500)

    channels = [
        ("Phone",      rb.get("phone",      {})),
        ("Email",      rb.get("email",      {})),
        ("IP Address", rb.get("ip_address", {})),
        ("Address",    rb.get("address",    {})),
    ]
    cols = st.columns(4)
    for col, (ch_name, ch_data) in zip(cols, channels):
        ch_score = ch_data.get("risk_score", 0.0)
        ch_level = ch_data.get("risk_level", "")
        ch_value = ch_data.get("value", "")
        with col:
            st.markdown(f"**{ch_name}**")
            st.markdown(_inline_bar(ch_score), unsafe_allow_html=True)
            st.markdown(_badge(ch_level), unsafe_allow_html=True)
            if ch_value:
                st.caption(ch_value)

    if signals and signals != ["No critical fraud signals detected"]:
        st.markdown("**Fraud signals:**")
        for s in signals:
            st.markdown(f"⚠️ {s}")
    else:
        st.success("No critical fraud signals detected.")

# ──────────────────────────────────────────────
# AGENT RUNNER
# ──────────────────────────────────────────────

def run_agent(user_query: str) -> list[dict]:
    """Run the async agent in a background thread and return all events."""
    result_queue: queue.Queue = queue.Queue()

    def _worker() -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        events: list[dict] = []
        try:
            async def _drain():
                async for event in stream_agent(user_query):
                    events.append(event)
            loop.run_until_complete(_drain())
        except Exception as e:
            events.append({"type": "error", "message": str(e)})
        finally:
            loop.close()
            result_queue.put(events)

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
    with st.spinner(""):
        t.join()
    return result_queue.get()


def _extract_risk_data(tool_events: list[dict]) -> dict | None:
    """Pull the first valid risk record out of tool results."""
    for event in tool_events:
        if event["type"] != "tool_result" or event["is_error"]:
            continue
        try:
            parsed = json.loads(event["content"])
            if not parsed.get("found"):
                continue
            if event["tool_name"] == "lookup_person" and parsed.get("records"):
                return parsed["records"][0]
            if event["tool_name"] == "get_risk_analysis":
                return parsed
        except Exception:
            pass
    return None

# ──────────────────────────────────────────────
# RENDER STORED MESSAGE (history replay)
# ──────────────────────────────────────────────

def render_assistant_message(msg: dict) -> None:
    if msg.get("content"):
        st.markdown(msg["content"])
    if msg.get("risk_data"):
        render_risk_card(msg["risk_data"])

# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────

def render_sidebar() -> None:
    with st.sidebar:
        st.title("🔍 Fraud Detection")
        st.caption(f"Model: **{agent_core.MODEL}**  \nEndpoint: `{agent_core.OLLAMA_URL}`")
        st.divider()

        low      = sum(1 for p in PEOPLE if p["overall_risk"] < 100)
        medium   = sum(1 for p in PEOPLE if 100 <= p["overall_risk"] < 250)
        high     = sum(1 for p in PEOPLE if 250 <= p["overall_risk"] < 400)
        critical = sum(1 for p in PEOPLE if p["overall_risk"] >= 400)

        st.markdown("**Database**")
        c1, c2 = st.columns(2)
        c1.metric("Records", len(PEOPLE))
        c2.metric("Critical", critical)

        st.markdown(
            f"""
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:8px 0">
              <div style="background:#d4edda;border-radius:8px;padding:8px;text-align:center">
                <div style="font-size:1.3em;font-weight:700;color:#155724">{low}</div>
                <div style="font-size:0.72em;color:#155724">Low</div>
              </div>
              <div style="background:#fff3cd;border-radius:8px;padding:8px;text-align:center">
                <div style="font-size:1.3em;font-weight:700;color:#856404">{medium}</div>
                <div style="font-size:0.72em;color:#856404">Medium</div>
              </div>
              <div style="background:#ffe0b2;border-radius:8px;padding:8px;text-align:center">
                <div style="font-size:1.3em;font-weight:700;color:#e65100">{high}</div>
                <div style="font-size:0.72em;color:#e65100">High</div>
              </div>
              <div style="background:#f8d7da;border-radius:8px;padding:8px;text-align:center">
                <div style="font-size:1.3em;font-weight:700;color:#721c24">{critical}</div>
                <div style="font-size:0.72em;color:#721c24">Critical</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()
        st.markdown("**Try asking:**")
        st.markdown(
            "- `Check Carlos Mendez`\n"
            "- `Is alice.harmon@gmail.com safe?`\n"
            "- `Look up IP 185.220.101.66`\n"
            "- `Run a check on +1-901-555-4848`\n"
            "- `Who is the highest risk person?`"
        )

        st.divider()
        if st.button("🗑️ Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

def main() -> None:
    render_sidebar()

    st.title("Fraud Detection Agent")
    st.caption("Ask about any person by name, email, phone, IP, or address.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "user":
                st.markdown(msg["content"])
            else:
                render_assistant_message(msg)

    # Input
    user_input = st.chat_input("Ask about a person, email, IP, or phone number...")
    if not user_input:
        return

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        events = run_agent(user_input)

        tool_events:   list[dict] = []
        response_text: str        = ""

        for event in events:
            etype = event["type"]
            if etype in ("tool_call", "tool_result"):
                tool_events.append(event)
            elif etype == "response":
                response_text = event["text"]
            elif etype == "error":
                st.error(event["message"])

        risk_data = _extract_risk_data(tool_events)

        if response_text:
            st.markdown(response_text)
        if risk_data:
            render_risk_card(risk_data)

        st.session_state.messages.append({
            "role":        "assistant",
            "content":     response_text,
            "tool_events": tool_events,
            "risk_data":   risk_data,
        })


if __name__ == "__main__":
    main()
