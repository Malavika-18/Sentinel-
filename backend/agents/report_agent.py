import json
from agents.gemma_client import call_gemma

REPORT_SYSTEM_PROMPT = """
You are a compliance report writer. You are given the full findings from a
completed transaction risk review — the transaction itself, what the Evader
agent was testing, what the Detector agent concluded, and the Adjudicator's
verdict.

Your job is to convert these structured findings into a clear, professional
compliance report a human reviewer can act on immediately.

CRITICAL RULE: Every claim in your report must be directly traceable to the
data provided. Do not invent facts, figures, or context that isn't present
in the findings. If something is uncertain, say so explicitly rather than
guessing.

Respond ONLY in valid JSON, in this exact format, with no extra text:

{
  "case_id": "<short generated case reference like SNT-2026-0001>",
  "headline": "<one sentence summary of the finding>",
  "risk_level": "Low" or "Medium" or "High",
  "summary": "<2-3 sentence plain-language summary of what was found>",
  "key_findings": ["<finding 1, tied to specific data>", "<finding 2>"],
  "recommended_action": "<one clear, specific next step for the reviewer>",
  "regulatory_reference": "<the specific RBI/KYC guideline this relates to>"
}
"""

def generate_report(round_data: dict):
    prompt = f"""
Case findings to convert into a report:

Transaction:
{json.dumps(round_data.get("evader", {}).get("transaction", {}), indent=2)}

Detector's analysis:
{json.dumps(round_data.get("detector", {}), indent=2)}

Adjudicator's verdict:
{json.dumps(round_data.get("verdict", {}), indent=2)}

Round outcome: {round_data.get("outcome")}
Risk category under review: {round_data.get("risk_category")}

Generate the compliance report now, following the JSON format exactly.
"""
    return call_gemma(REPORT_SYSTEM_PROMPT, prompt)
