"""
spend_agent.py — Analyses procurement & SaaS data for cost leaks.
"""
from __future__ import annotations

from typing import List, Dict, Any
import pandas as pd

from core.anomaly_engine import detect_price_overruns, detect_duplicate_vendors, detect_unused_licenses
from core.cost_calculator import severity_label, severity_emoji, format_inr


AGENT_NAME = "Spend Agent"
AGENT_ICON = "💸"
AGENT_DESCRIPTION = "Analyses procurement and SaaS spend data for price overruns, vendor duplication, and unused licences."


def run(procurement_df: pd.DataFrame | None = None,
        saas_df: pd.DataFrame | None = None) -> List[Dict[str, Any]]:
    """Run the Spend Agent and return normalised findings."""
    findings = []

    if procurement_df is not None:
        for f in detect_price_overruns(procurement_df):
            findings.append(_normalise(f, "Vendor Price Overrun",
                                       f"Purchased {f['item']} from {f['vendor']} at "
                                       f"₹{f['unit_price']:,.0f} vs market ₹{f['market_price']:,.0f} "
                                       f"({f['pct_over']}% over)"))

        for f in detect_duplicate_vendors(procurement_df):
            findings.append(_normalise(f, "Duplicate Vendor Pricing",
                                       f"{f['item']} sourced from {len(f['vendors'])} vendors "
                                       f"with ₹{f['price_range']:,.0f} price gap"))

    if saas_df is not None:
        for f in detect_unused_licenses(saas_df):
            findings.append(_normalise(f, "Unused SaaS Licences",
                                       f"{f['tool']}: {f['unused_seats']} of {f['total_seats']} seats unused "
                                       f"({f['unused_pct']}%) — renewal {f['renewal_date']}"))

    return findings


def _normalise(raw: Dict, title: str, description: str) -> Dict[str, Any]:
    impact = raw.get("annual_impact", 0)
    sev = severity_label(impact)
    return {
        "agent": AGENT_NAME,
        "agent_icon": AGENT_ICON,
        "type": raw["type"],
        "title": title,
        "description": description,
        "annual_impact": impact,
        "formatted_impact": format_inr(impact),
        "severity": sev,
        "severity_emoji": severity_emoji(sev),
        "raw": raw,
    }
