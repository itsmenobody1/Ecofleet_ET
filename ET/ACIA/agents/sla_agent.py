"""
sla_agent.py — Monitors tickets for SLA breach risk.
"""
from __future__ import annotations

from typing import List, Dict, Any
import pandas as pd

from core.anomaly_engine import detect_sla_risks
from core.cost_calculator import severity_label, severity_emoji, format_inr


AGENT_NAME = "SLA Agent"
AGENT_ICON = "⏱️"
AGENT_DESCRIPTION = "Monitors support tickets for SLA breach risk and calculates penalty exposure."


def run(tickets_df: pd.DataFrame | None = None) -> List[Dict[str, Any]]:
    if tickets_df is None:
        return []

    findings = []
    for f in detect_sla_risks(tickets_df):
        if f["breached"]:
            title = f"SLA BREACHED — {f['title']}"
            desc = (f"Ticket {f['ticket_id']} has exceeded SLA by "
                    f"{abs(f['remaining_minutes'])} mins. "
                    f"Customer: {f['customer']}. Penalty: ₹{f['penalty']:,}")
        else:
            title = f"SLA Breach Risk — {f['title']}"
            desc = (f"Ticket {f['ticket_id']}: {f['remaining_minutes']} mins remaining "
                    f"of {f['sla_hours']}h SLA ({f['pct_elapsed']}% elapsed). "
                    f"Customer: {f['customer']}")

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
