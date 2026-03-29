"""
prompts.py — All LLM prompt templates in one place.
"""

SYSTEM_PROMPT = """You are ACIA, an Autonomous Cost Intelligence Agent for enterprise operations.
You analyze enterprise data to identify cost leakages, inefficiencies, and risks.
Always respond with structured JSON when requested.
Be concise, data-driven, and quantify findings in Indian Rupees (₹)."""


FINDING_EXPLANATION_PROMPT = """
You are analyzing an enterprise cost finding. Provide a detailed explanation.

Finding Details:
- Category: {category}
- Title: {title}
- Detected Value: {detected_value}
- Baseline Value: {baseline_value}
- Annual Impact: ₹{annual_impact}
- Raw Data: {raw_data}

Respond in the following JSON format:
{{
  "why_detected": "2-3 sentence explanation of why this was flagged",
  "cost_math": "Step-by-step calculation showing how ₹{annual_impact} was derived",
  "playbook": ["Step 1: ...", "Step 2: ...", "Step 3: ..."],
  "risk_level": "HIGH|MEDIUM|LOW",
  "confidence": 0.0-1.0
}}
"""

SUMMARY_DASHBOARD_PROMPT = """
Summarize these {count} enterprise cost findings into an executive brief (2-3 sentences).
Total leakage detected: ₹{total_leakage}
Top categories: {categories}

Be direct and impactful.
"""

APPROVAL_EMAIL_PROMPT = """
Draft a professional approval-action email for the following finding:
Title: {title}
Impact: ₹{annual_impact}/year
Recommended Action: {action}

Keep it under 100 words, professional tone.
"""
