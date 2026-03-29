"""
helpers.py — Shared utility functions.
"""
from __future__ import annotations

from typing import List, Dict, Any
from datetime import datetime

from core.cost_calculator import format_inr, severity_emoji


def total_leakage(findings: List[Dict]) -> float:
    return sum(f.get("annual_impact", 0) for f in findings)


def findings_by_agent(findings: List[Dict]) -> Dict[str, List[Dict]]:
    result: Dict[str, List[Dict]] = {}
    for f in findings:
        agent = f.get("agent", "Unknown")
        result.setdefault(agent, []).append(f)
    return result


def findings_by_severity(findings: List[Dict]) -> Dict[str, int]:
    counts: Dict[str, int] = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for f in findings:
        sev = f.get("severity", "LOW")
        counts[sev] = counts.get(sev, 0) + 1
    return counts


def sort_findings(findings: List[Dict], by: str = "annual_impact") -> List[Dict]:
    return sorted(findings, key=lambda x: x.get(by, 0), reverse=True)


def finding_feed_line(f: Dict) -> str:
    emoji = f.get("severity_emoji", "⚪")
    title = f.get("title", "")
    impact = format_inr(f.get("annual_impact", 0))
    agent  = f.get("agent", "")
    return f"{emoji} **{title}** — {impact}/year  _{agent}_"


def timestamp_now() -> str:
    return datetime.now().strftime("%I:%M %p")
