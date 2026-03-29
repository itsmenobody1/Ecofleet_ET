"""
resource_agent.py — Detects idle cloud infrastructure.
"""
from __future__ import annotations

from typing import List, Dict, Any
import pandas as pd

from core.anomaly_engine import detect_idle_servers
from core.cost_calculator import severity_label, severity_emoji, format_inr


AGENT_NAME = "Resource Agent"
AGENT_ICON = "🖥️"
AGENT_DESCRIPTION = "Scans cloud infrastructure for idle servers and over-provisioned resources."


def run(cloud_df: pd.DataFrame | None = None) -> List[Dict[str, Any]]:
    if cloud_df is None:
        return []

    findings = []
    for f in detect_idle_servers(cloud_df):
        title = f"Idle Server — {f['server']}"
        desc = (f"{f['server']} ({f['instance_type']}, {f['region']}) "
                f"running at {f['cpu_pct']}% CPU / {f['mem_pct']}% RAM. "
                f"Last active: {f['last_active']}. Monthly cost: ₹{f['monthly_cost']:,}")

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
