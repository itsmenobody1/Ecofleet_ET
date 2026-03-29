"""
cost_calculator.py — ₹ impact math engine for all finding types.
"""
from __future__ import annotations

from config.settings import CURRENCY_SYMBOL


def overpay_annual(unit_price: float, market_price: float, quantity: float,
                   purchases_per_year: int = 1) -> float:
    """Annual overpayment vs. market price."""
    return max(0.0, (unit_price - market_price) * quantity * purchases_per_year)


def idle_resource_annual(monthly_cost: float, idle_months: int = 12) -> float:
    """Cost of running an idle resource for a given number of months."""
    return monthly_cost * idle_months


def unused_seats_annual(annual_cost: float, total_seats: int,
                        active_users: int) -> float:
    """Annual cost of unused SaaS seats."""
    if total_seats == 0:
        return 0.0
    unused = max(0, total_seats - active_users)
    per_seat_annual = annual_cost / total_seats
    return unused * per_seat_annual


def sla_breach_penalty(estimated_penalty: float, probability: float = 1.0) -> float:
    """Expected penalty cost if SLA breaches."""
    return estimated_penalty * probability


def duplicate_invoice_loss(amount: float, occurrences: int = 2) -> float:
    """Total extra spend from duplicate invoices (n-1 extra payments)."""
    return amount * (occurrences - 1)


def format_inr(amount: float) -> str:
    """Format a number as Indian Rupee string with lakh/crore shorthand."""
    if amount >= 1_00_00_000:
        return f"{CURRENCY_SYMBOL}{amount / 1_00_00_000:.2f} Cr"
    if amount >= 1_00_000:
        return f"{CURRENCY_SYMBOL}{amount / 1_00_000:.2f} L"
    return f"{CURRENCY_SYMBOL}{amount:,.0f}"


def severity_label(annual_impact: float) -> str:
    """Return HIGH / MEDIUM / LOW based on annual ₹ impact."""
    if annual_impact >= 5_00_000:
        return "HIGH"
    if annual_impact >= 1_00_000:
        return "MEDIUM"
    return "LOW"


def severity_emoji(severity: str) -> str:
    return {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🔵"}.get(severity, "⚪")
