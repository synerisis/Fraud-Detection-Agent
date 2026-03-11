"""
Fraud Detection MCP Server

Exposes fraud risk data via:
  Tools     - search, lookup, and analyze people
  Resources - database overview and schema
  Prompts   - analysis templates
"""

import json
from difflib import SequenceMatcher
from mcp.server.fastmcp import FastMCP
from data import PEOPLE, get_risk_label, get_overall_risk_label

mcp = FastMCP("Fraud Detection Server")


# ──────────────────────────────────────────────
# TOOLS
# ──────────────────────────────────────────────

@mcp.tool()
def lookup_person(query: str) -> str:
    """
    Primary tool. Look up any person by name, email, phone number, IP address,
    or physical address and return their complete profile with full fraud risk
    analysis in a single call. Use this for every question about a person or
    contact identifier. Returns identity details, per-channel risk scores
    (phone, email, IP, address), overall risk level, and fraud signals.
    """
    q = query.lower().strip()
    matches = []

    for person in PEOPLE:
        fields = [
            person["name"].lower(),
            person["phone"].lower(),
            person["email"].lower(),
            person["ip"].lower(),
            person["address"].lower(),
        ]
        if any(q in field for field in fields):
            matches.append(person)
            continue
        if SequenceMatcher(None, q, person["name"].lower()).ratio() > 0.7:
            matches.append(person)

    if not matches:
        return json.dumps({"found": False, "message": f"No records found matching '{query}'"})

    records = []
    for p in matches:
        signals = []
        if p["ip_risk"] >= 0.7:
            signals.append(f"IP {p['ip']} associated with fraud networks or VPN/Tor exit nodes")
        if p["email_risk"] >= 0.7:
            signals.append(f"Email {p['email']} uses a disposable/anonymous mail service")
        if p["phone_risk"] >= 0.7:
            signals.append(f"Phone {p['phone']} has high fraud association")
        if p["address_risk"] >= 0.6:
            signals.append(f"Address shows anomalous patterns")

        records.append({
            "id": p["id"],
            "name": p["name"],
            "phone": p["phone"],
            "email": p["email"],
            "ip_address": p["ip"],
            "address": p["address"],
            "risk_breakdown": {
                "phone":      {"value": p["phone"],   "risk_score": p["phone_risk"],   "risk_level": get_risk_label(p["phone_risk"])},
                "email":      {"value": p["email"],   "risk_score": p["email_risk"],   "risk_level": get_risk_label(p["email_risk"])},
                "ip_address": {"value": p["ip"],      "risk_score": p["ip_risk"],      "risk_level": get_risk_label(p["ip_risk"])},
                "address":    {"value": p["address"], "risk_score": p["address_risk"], "risk_level": get_risk_label(p["address_risk"])},
            },
            "overall_risk": {
                "score": p["overall_risk"],
                "max_score": 500,
                "level": get_overall_risk_label(p["overall_risk"]),
            },
            "fraud_signals": signals if signals else ["No critical fraud signals detected"],
        })

    return json.dumps({"found": True, "count": len(records), "records": records}, indent=2)


@mcp.tool()
def search_person(query: str) -> str:
    """
    Search for a person by any identifier: name, phone number, email address,
    IP address, or physical address. Returns all matching records with full
    risk scores. Use this as the primary lookup tool.
    """
    q = query.lower().strip()
    matches = []

    for person in PEOPLE:
        fields = [
            person["name"].lower(),
            person["phone"].lower(),
            person["email"].lower(),
            person["ip"].lower(),
            person["address"].lower(),
        ]
        # Exact substring match
        if any(q in field for field in fields):
            matches.append(person)
            continue
        # Fuzzy name match (handles minor typos)
        name_ratio = SequenceMatcher(None, q, person["name"].lower()).ratio()
        if name_ratio > 0.7:
            matches.append(person)

    if not matches:
        return json.dumps({"found": False, "message": f"No records found matching '{query}'"})

    results = []
    for p in matches:
        results.append(_format_person(p))

    return json.dumps({"found": True, "count": len(results), "records": results}, indent=2)


@mcp.tool()
def get_person_by_id(person_id: int) -> str:
    """
    Retrieve full details for a specific person by their numeric ID (1-50).
    Returns all fields including contact info and all risk scores.
    """
    person = next((p for p in PEOPLE if p["id"] == person_id), None)
    if not person:
        return json.dumps({"found": False, "message": f"No person found with ID {person_id}"})
    return json.dumps({"found": True, "record": _format_person(person)}, indent=2)


@mcp.tool()
def get_risk_analysis(person_id: int) -> str:
    """
    Get a detailed fraud risk breakdown for a specific person (by ID).
    Returns individual risk scores for phone, email, IP, and address,
    the overall risk score (1-500), risk level labels, and a summary
    of which signals are most concerning.
    """
    person = next((p for p in PEOPLE if p["id"] == person_id), None)
    if not person:
        return json.dumps({"found": False, "message": f"No person found with ID {person_id}"})

    signals = []
    if person["ip_risk"] >= 0.7:
        signals.append(f"IP address {person['ip']} is associated with known fraud networks or VPN/Tor exit nodes")
    if person["email_risk"] >= 0.7:
        signals.append(f"Email {person['email']} uses a disposable/anonymous mail service")
    if person["phone_risk"] >= 0.7:
        signals.append(f"Phone {person['phone']} has high fraud association")
    if person["address_risk"] >= 0.6:
        signals.append(f"Physical address shows anomalous patterns")

    analysis = {
        "found": True,
        "person_id": person["id"],
        "name": person["name"],
        "risk_breakdown": {
            "phone": {
                "value": person["phone"],
                "risk_score": person["phone_risk"],
                "risk_level": get_risk_label(person["phone_risk"])
            },
            "email": {
                "value": person["email"],
                "risk_score": person["email_risk"],
                "risk_level": get_risk_label(person["email_risk"])
            },
            "ip_address": {
                "value": person["ip"],
                "risk_score": person["ip_risk"],
                "risk_level": get_risk_label(person["ip_risk"])
            },
            "address": {
                "value": person["address"],
                "risk_score": person["address_risk"],
                "risk_level": get_risk_label(person["address_risk"])
            },
        },
        "overall_risk": {
            "score": person["overall_risk"],
            "max_score": 500,
            "level": get_overall_risk_label(person["overall_risk"]),
        },
        "fraud_signals": signals if signals else ["No critical fraud signals detected"],
    }
    return json.dumps(analysis, indent=2)


@mcp.tool()
def list_high_risk_persons(min_overall_risk: int = 300) -> str:
    """
    List all persons whose overall risk score exceeds a given threshold.
    Default threshold is 300 (out of 500). Returns names, IDs, and scores.
    Useful for generating watchlists or batch reviews.
    """
    high_risk = [p for p in PEOPLE if p["overall_risk"] >= min_overall_risk]
    high_risk.sort(key=lambda x: x["overall_risk"], reverse=True)

    if not high_risk:
        return json.dumps({
            "count": 0,
            "message": f"No persons found with overall risk >= {min_overall_risk}"
        })

    return json.dumps({
        "threshold": min_overall_risk,
        "count": len(high_risk),
        "persons": [
            {
                "id": p["id"],
                "name": p["name"],
                "overall_risk": p["overall_risk"],
                "risk_level": get_overall_risk_label(p["overall_risk"]),
            }
            for p in high_risk
        ]
    }, indent=2)


@mcp.tool()
def get_database_statistics() -> str:
    """
    Return aggregate statistics about the fraud database:
    total records, risk distribution breakdown, average scores,
    and counts by risk tier. Useful for getting a quick overview.
    """
    total = len(PEOPLE)
    low = sum(1 for p in PEOPLE if p["overall_risk"] < 100)
    medium = sum(1 for p in PEOPLE if 100 <= p["overall_risk"] < 250)
    high = sum(1 for p in PEOPLE if 250 <= p["overall_risk"] < 400)
    critical = sum(1 for p in PEOPLE if p["overall_risk"] >= 400)

    avg_overall = sum(p["overall_risk"] for p in PEOPLE) / total
    avg_ip = sum(p["ip_risk"] for p in PEOPLE) / total
    avg_email = sum(p["email_risk"] for p in PEOPLE) / total
    avg_phone = sum(p["phone_risk"] for p in PEOPLE) / total
    avg_address = sum(p["address_risk"] for p in PEOPLE) / total

    return json.dumps({
        "total_records": total,
        "risk_distribution": {
            "low_risk": {"count": low, "range": "1-99", "percentage": f"{low/total*100:.1f}%"},
            "medium_risk": {"count": medium, "range": "100-249", "percentage": f"{medium/total*100:.1f}%"},
            "high_risk": {"count": high, "range": "250-399", "percentage": f"{high/total*100:.1f}%"},
            "critical_risk": {"count": critical, "range": "400-500", "percentage": f"{critical/total*100:.1f}%"},
        },
        "average_scores": {
            "overall_risk": round(avg_overall, 1),
            "ip_risk": round(avg_ip, 2),
            "email_risk": round(avg_email, 2),
            "phone_risk": round(avg_phone, 2),
            "address_risk": round(avg_address, 2),
        },
    }, indent=2)


# ──────────────────────────────────────────────
# RESOURCES
# ──────────────────────────────────────────────

@mcp.resource("fraud://database/overview")
def database_overview() -> str:
    """High-level overview of the fraud database contents and statistics."""
    total = len(PEOPLE)
    critical = [p for p in PEOPLE if p["overall_risk"] >= 400]
    low_risk = [p for p in PEOPLE if p["overall_risk"] < 100]

    return f"""# Fraud Detection Database Overview

Total Records: {total} individuals

## Risk Distribution
- Low Risk (1-99): {len(low_risk)} persons
- Medium Risk (100-249): {sum(1 for p in PEOPLE if 100 <= p["overall_risk"] < 250)} persons
- High Risk (250-399): {sum(1 for p in PEOPLE if 250 <= p["overall_risk"] < 400)} persons
- Critical Risk (400-500): {len(critical)} persons

## Top 5 Highest Risk Individuals
{chr(10).join(f"  {i+1}. {p['name']} — Score: {p['overall_risk']}/500 ({get_overall_risk_label(p['overall_risk'])})"
              for i, p in enumerate(sorted(PEOPLE, key=lambda x: x['overall_risk'], reverse=True)[:5]))}

## Data Fields Per Record
- Identity: name, phone, email, IP address, physical address
- Risk Scores: phone_risk, email_risk, address_risk, ip_risk (each 0.0–1.0)
- Overall Risk Score: 1–500
"""


@mcp.resource("fraud://database/schema")
def database_schema() -> str:
    """Schema and field descriptions for the fraud database."""
    return """{
  "schema": {
    "id": "Unique integer identifier (1-50)",
    "name": "Full legal name",
    "phone": "Phone number in E.164 format",
    "email": "Email address",
    "ip": "Last known IP address (IPv4)",
    "address": "Physical mailing address",
    "phone_risk": "Phone fraud risk score: 0.0 (clean) to 1.0 (highly suspicious)",
    "email_risk": "Email fraud risk score: 0.0 to 1.0. High scores indicate disposable/anonymous mail services",
    "address_risk": "Address fraud risk score: 0.0 to 1.0. Anomalous or commercial addresses score higher",
    "ip_risk": "IP fraud risk score: 0.0 to 1.0. Tor/VPN/proxy IPs score 0.7+",
    "overall_risk": "Composite risk score 1-500. <100=Low, 100-249=Medium, 250-399=High, 400-500=Critical"
  }
}"""


# ──────────────────────────────────────────────
# PROMPTS
# ──────────────────────────────────────────────

@mcp.prompt()
def analyze_fraud_risk(identifier: str) -> str:
    """
    Generate a structured fraud risk analysis prompt for a given identifier
    (name, email, phone, IP, or address).
    """
    return f"""You are a fraud analyst. A user has submitted the following identifier for review:

Identifier: {identifier}

Please:
1. Search the fraud database for this identifier using the search_person tool
2. If found, retrieve a detailed risk analysis using get_risk_analysis
3. Provide a clear, structured assessment covering:
   - Who this person is
   - Their risk scores across all channels (phone, email, IP, address)
   - Overall risk level and score
   - Specific fraud signals detected
   - A recommended action (approve / review / decline / escalate)

Be concise but thorough. Present risk scores as percentages where helpful."""


@mcp.prompt()
def explain_risk_scores() -> str:
    """
    Return a prompt that explains the fraud scoring methodology.
    """
    return """Explain the fraud risk scoring system used in this database:

- Individual channel scores (phone, email, IP, address) range from 0.0 to 1.0
  - 0.0–0.29: Low risk — normal, verified sources
  - 0.30–0.59: Medium risk — some anomalies, needs review
  - 0.60–1.0: High risk — strong fraud signals

- Overall risk score ranges from 1 to 500
  - 1–99: Low Risk
  - 100–249: Medium Risk
  - 250–399: High Risk
  - 400–500: Critical Risk

High IP risk often indicates Tor exit nodes, VPN services, or known fraud infrastructure.
High email risk indicates disposable mail services (mailinator, guerrillamail, throwaway, etc.).
High phone risk indicates VOIP numbers or numbers associated with prior fraud.
High address risk indicates commercial mail drops, frequent address changes, or known fraud addresses."""


# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────

def _format_person(p: dict) -> dict:
    return {
        "id": p["id"],
        "name": p["name"],
        "phone": p["phone"],
        "email": p["email"],
        "ip_address": p["ip"],
        "address": p["address"],
        "risk_scores": {
            "phone": {"score": p["phone_risk"], "level": get_risk_label(p["phone_risk"])},
            "email": {"score": p["email_risk"], "level": get_risk_label(p["email_risk"])},
            "ip":    {"score": p["ip_risk"],    "level": get_risk_label(p["ip_risk"])},
            "address": {"score": p["address_risk"], "level": get_risk_label(p["address_risk"])},
        },
        "overall_risk": {
            "score": p["overall_risk"],
            "level": get_overall_risk_label(p["overall_risk"]),
        },
    }


if __name__ == "__main__":
    mcp.run()
