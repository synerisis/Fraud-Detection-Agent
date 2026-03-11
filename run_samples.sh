#!/bin/bash
# Run sample fraud detection queries
# Usage: ANTHROPIC_API_KEY=sk-ant-... ./run_samples.sh
#    or: cp .env.example .env  # edit .env with your key, then ./run_samples.sh

set -e
cd "$(dirname "$0")"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  FRAUD DETECTION AGENT — Sample Queries"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "Sample 1: Look up by email (high-risk user)"
python3 agent.py "Is carlos.mendez99@yahoo.com safe to approve?"

echo ""
echo "Sample 2: Look up by name (low-risk user)"
python3 agent.py "What is the fraud risk for Mei Zhang?"

echo ""
echo "Sample 3: Look up by IP address"
python3 agent.py "Flag check on IP 185.220.101.66"

echo ""
echo "Sample 4: Look up by phone number"
python3 agent.py "Run a risk check on +1-901-555-4848"

echo ""
echo "Sample 5: Combined query"
python3 agent.py "Check Alice Harmon at alice.harmon@gmail.com — is she low risk?"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "All samples complete. Run 'python3 agent.py' for interactive mode."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
