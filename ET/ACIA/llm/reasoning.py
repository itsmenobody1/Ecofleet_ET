"""
reasoning.py — Converts raw agent findings into LLM-enriched explanations
               with rule-based fallbacks when no LLM is available.
"""
from __future__ import annotations

from typing import Dict, Any

from config.prompts import FINDING_EXPLANATION_PROMPT
from core.cost_calculator import format_inr
from llm.llm_client import chat_completion, parse_json_response


# ── Fallback Templates (no LLM) ───────────────────────────────────────────────

_FALLBACK_PLAYBOOKS: Dict[str, list] = {
    "price_overrun": [
        "Step 1: Pull latest market quotes from 3 alternative vendors.",
        "Step 2: Send renegotiation request to current vendor with benchmark data.",
        "Step 3: Update contract if vendor agrees; else switch supplier.",
    ],
    "duplicate_vendor_pricing": [
        "Step 1: Consolidate purchase orders to the lowest-cost verified supplier.",
        "Step 2: Blacklist higher-priced vendors for this SKU.",
        "Step 3: Update procurement policy to enforce single-vendor per category.",
    ],
    "idle_server": [
        "Step 1: Confirm with server owner that the instance has no scheduled jobs.",
        "Step 2: Take a snapshot backup of the server.",
        "Step 3: Terminate or stop the instance; set 30-day auto-delete schedule.",
    ],
    "unused_licenses": [
        "Step 1: Export inactive user list from the SaaS admin panel.",
        "Step 2: Send 7-day notice to users; reclaim seats after no activity.",
        "Step 3: Negotiate reduced seat count at next renewal.",
    ],
    "sla_breach_risk": [
        "Step 1: Immediately escalate ticket to Tier-2 on-call engineer.",
        "Step 2: Notify customer with ETA update to maintain goodwill.",
        "Step 3: Post-mortem: root-cause SLA near-miss within 48 hours.",
    ],
    "duplicate_invoice": [
        "Step 1: Flag both invoice entries in the AP system as duplicates.",
        "Step 2: Contact vendor accounts team to issue a credit note.",
        "Step 3: Implement PO-matching rule to block future duplicate payments.",
    ],
}

_FALLBACK_WHY: Dict[str, str] = {
    "price_overrun": "The unit purchase price exceeds the current market benchmark price by the configured threshold, indicating potential overpayment or an outdated contract.",
    "duplicate_vendor_pricing": "The same item is being procured from multiple vendors at significantly different price points, creating arbitrage waste and supply-chain complexity.",
    "idle_server": "Server CPU and memory utilisation have both remained below the idle threshold, indicating no meaningful workload is running while the instance is accruing costs.",
    "unused_licenses": "A significant percentage of purchased SaaS seats are unassigned or inactive, meaning the organisation is paying for capacity no one is using.",
    "sla_breach_risk": "The ticket has consumed more than 80% of its allotted SLA window without reaching a resolved state, putting the organisation at risk of contractual penalty.",
    "duplicate_invoice": "The same invoice number from the same vendor appears multiple times in the payables ledger with matching amounts, indicating a duplicate payment was processed.",
}


def enrich_finding(finding: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns enriched explanation for a finding.
    Tries LLM first; falls back to rule-based templates.
    """
    ftype = finding.get("type", "unknown")
    raw   = finding.get("raw", {})
    impact = finding.get("annual_impact", 0)

    prompt = FINDING_EXPLANATION_PROMPT.format(
        category=finding.get("agent", ""),
        title=finding.get("title", ""),
        detected_value=raw.get("unit_price", raw.get("cpu_pct", raw.get("unused_pct", "N/A"))),
        baseline_value=raw.get("market_price", raw.get("sla_hours", raw.get("total_seats", "N/A"))),
        annual_impact=f"{impact:,.0f}",
        raw_data=str(raw)[:500],
    )

    llm_raw  = chat_completion(prompt)
    llm_data = parse_json_response(llm_raw)

    if llm_data:
        return {
            "why_detected":  llm_data.get("why_detected", ""),
            "cost_math":     llm_data.get("cost_math", ""),
            "playbook":      llm_data.get("playbook", []),
            "risk_level":    llm_data.get("risk_level", finding.get("severity", "MEDIUM")),
            "confidence":    llm_data.get("confidence", 0.85),
            "source": "llm",
        }

    # Fallback
    cost_math = _build_cost_math(ftype, raw, impact)
    return {
        "why_detected": _FALLBACK_WHY.get(ftype, "Anomaly detected by rule engine."),
        "cost_math":    cost_math,
        "playbook":     _FALLBACK_PLAYBOOKS.get(ftype, ["Review finding and take manual action."]),
        "risk_level":   finding.get("severity", "MEDIUM"),
        "confidence":   0.90,
        "source": "rules",
    }


def _build_cost_math(ftype: str, raw: Dict, impact: float) -> str:
    if ftype == "price_overrun":
        diff = raw.get("unit_price", 0) - raw.get("market_price", 0)
        qty  = raw.get("quantity", 1)
        return (f"Price gap: ₹{raw.get('unit_price',0):,} − ₹{raw.get('market_price',0):,} "
                f"= ₹{diff:,}/unit × {qty} units × 4 purchases/year = {format_inr(impact)}/year")
    if ftype == "idle_server":
        mc = raw.get("monthly_cost", 0)
        return f"Monthly cost: ₹{mc:,} × 12 months = {format_inr(impact)}/year wasted"
    if ftype == "unused_licenses":
        seats = raw.get("unused_seats", 0)
        annual = raw.get("annual_cost", 0)
        total  = raw.get("total_seats", 1)
        per_seat = annual / total if total else 0
        return (f"{seats} unused seats × ₹{per_seat:,.0f}/seat/year "
                f"= {format_inr(impact)}/year wasted")
    if ftype == "sla_breach_risk":
        return f"Contractual penalty exposure if SLA breached: {format_inr(impact)}"
    if ftype == "duplicate_invoice":
        amt = raw.get("amount_per", 0)
        occ = raw.get("occurrences", 2)
        return f"₹{amt:,} × {occ-1} extra payment(s) = {format_inr(impact)} lost"
    if ftype == "duplicate_vendor_pricing":
        pr = raw.get("price_range", 0)
        qty = raw.get("total_quantity", 0)
        return (f"Price gap ₹{pr:,} × {qty} units × 2 orders/year = {format_inr(impact)}/year")
    return f"Estimated annual impact: {format_inr(impact)}"
