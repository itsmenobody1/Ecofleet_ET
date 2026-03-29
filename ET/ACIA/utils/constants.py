"""
constants.py — UI and domain constants.
"""

AGENT_INFO = {
    "Spend Agent":    {"icon": "💸", "color": "#f59e0b", "datasets": ["procurement", "saas_usage"]},
    "SLA Agent":      {"icon": "⏱️", "color": "#ef4444", "datasets": ["tickets"]},
    "Resource Agent": {"icon": "🖥️", "color": "#8b5cf6", "datasets": ["cloud_usage"]},
    "Finance Agent":  {"icon": "💰", "color": "#10b981", "datasets": ["invoices"]},
}

SEVERITY_COLORS = {
    "HIGH":   "#ef4444",
    "MEDIUM": "#f59e0b",
    "LOW":    "#3b82f6",
}

SEVERITY_BG = {
    "HIGH":   "rgba(239,68,68,0.12)",
    "MEDIUM": "rgba(245,158,11,0.12)",
    "LOW":    "rgba(59,130,246,0.12)",
}

DATASET_LABELS = {
    "procurement": "Procurement Data",
    "cloud_usage": "Cloud Usage",
    "saas_usage":  "SaaS Licences",
    "tickets":     "Support Tickets",
    "invoices":    "AP Invoices",
}

PAGE_NAMES = ["Dashboard", "Upload Data", "AI Findings", "Approvals", "Action Logs"]
