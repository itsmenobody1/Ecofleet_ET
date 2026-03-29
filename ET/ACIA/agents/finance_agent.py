"""
finance_agent.py — Detects duplicate invoices and payment anomalies.
"""
from __future__ import annotations

from typing import List, Dict, Any
import pandas as pd

from core.anomaly_engine import detect_duplicate_invoices
from core.cost_calculator import severity_label, severity_emoji, format_inr


AGENT_NAME = "Finance Agent"
AGENT_ICON = "💰"
AGENT_DESCRIPTION = "Scans AP invoices for duplicate payments, billing anomalies, and unapproved spend."


def run(invoices_df: pd.DataFrame | None = None) -> List[Dict[str, Any]]:
    if invoices_df is None:
        return []

    findings = []
    for f in detect_duplicate_invoices(invoices_df):
        title = f"Duplicate Invoice — {f['vendor']}"
        desc = (f"Invoice {f['invoice_number']} from {f['vendor']} "
                f"was processed {f['occurrences']}x. "
                f"Amount per invoice: ₹{f['amount_per']:,}. "
                f"Extra paid: ₹{f['annual_impact']:,} | Dept: {f['department']}")

        impact = f.get("annual_impact", 0)
        sev = severity_label(impact)
        findings.append({
            "agent": AGENT_NAME,
            "agent_icon": AGENT_ICON,
            "type": f["type"],
            "title": title,
            "description": desc,
            "annual_impact": impact,
            "formatted_impact": format_inr(impact),
            "severity": sev,
            "severity_emoji": severity_emoji(sev),
            "raw": f,
        })

    return findings
