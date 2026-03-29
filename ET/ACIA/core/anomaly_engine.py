"""
anomaly_engine.py — Rule-based + optional ML anomaly detection.
"""
from __future__ import annotations

import pandas as pd
import numpy as np
from typing import List, Dict, Any

from config.settings import (
    IDLE_CPU_THRESHOLD, IDLE_MEMORY_THRESHOLD,
    PRICE_DIFF_THRESHOLD_PCT, UNUSED_SEAT_THRESHOLD_PCT,
    DUPLICATE_INVOICE_TOLERANCE,
)


# ── Procurement Anomalies ─────────────────────────────────────────────────────

def detect_price_overruns(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Find purchases where unit_price > market_price by threshold %."""
    findings = []
    if df is None or df.empty or "unit_price_inr" not in df.columns or "market_price_inr" not in df.columns:
        return findings
    for _, row in df.iterrows():
        if pd.isna(row.get("unit_price_inr")) or pd.isna(row.get("market_price_inr")):
            continue
        pct_over = ((row["unit_price_inr"] - row["market_price_inr"])
                    / row["market_price_inr"] * 100)
        if pct_over >= PRICE_DIFF_THRESHOLD_PCT:
            overpay = (row["unit_price_inr"] - row["market_price_inr"]) * row.get("quantity", 1)
            findings.append({
                "type": "price_overrun",
                "vendor": row.get("vendor_name", "Unknown"),
                "item": row.get("item_description", ""),
                "unit_price": row["unit_price_inr"],
                "market_price": row["market_price_inr"],
                "pct_over": round(pct_over, 1),
                "quantity": row.get("quantity", 1),
                "overpay_total": overpay,
                "annual_impact": overpay * 4,  # assume quarterly purchase
            })
    return findings


def detect_duplicate_vendors(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Find same item bought from multiple vendors at different prices."""
    findings = []
    if df is None or df.empty or "item_description" not in df.columns or "vendor_name" not in df.columns or "unit_price_inr" not in df.columns:
        return findings
    grp = df.groupby("item_description")
    for item, group in grp:
        if len(group["vendor_name"].unique()) > 1:
            price_range = group["unit_price_inr"].max() - group["unit_price_inr"].min()
            if price_range > 0:
                total_qty = group["quantity"].sum() if "quantity" in group.columns else 0
                findings.append({
                    "type": "duplicate_vendor_pricing",
                    "item": item,
                    "vendors": list(group["vendor_name"].unique()),
                    "price_range": price_range,
                    "max_price": group["unit_price_inr"].max(),
                    "min_price": group["unit_price_inr"].min(),
                    "total_quantity": total_qty,
                    "annual_impact": price_range * total_qty * 2,
                })
    return findings


# ── Cloud Resource Anomalies ──────────────────────────────────────────────────

def detect_idle_servers(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Flag servers with CPU < threshold AND memory < threshold."""
    findings = []
    if df is None or df.empty:
        return findings
    for _, row in df.iterrows():
        cpu = row.get("cpu_usage_pct", 100)
        mem = row.get("memory_usage_pct", 100)
        if cpu <= IDLE_CPU_THRESHOLD and mem <= IDLE_MEMORY_THRESHOLD:
            findings.append({
                "type": "idle_server",
                "server": row.get("server_name", row.get("server_id", "")),
                "region": row.get("region", ""),
                "instance_type": row.get("instance_type", ""),
                "cpu_pct": cpu,
                "mem_pct": mem,
                "monthly_cost": row.get("monthly_cost_inr", 0),
                "annual_impact": row.get("monthly_cost_inr", 0) * 12,
                "last_active": str(row.get("last_active", "")),
                "environment": row.get("environment", ""),
            })
    return findings


# ── SaaS Usage Anomalies ──────────────────────────────────────────────────────

def detect_unused_licenses(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Find SaaS tools with >threshold% unused seats."""
    findings = []
    if df is None or df.empty:
        return findings
    for _, row in df.iterrows():
        total = row.get("total_seats", 0)
        active = row.get("active_users", 0)
        if total == 0:
            continue
        unused_pct = (total - active) / total * 100
        if unused_pct >= UNUSED_SEAT_THRESHOLD_PCT:
            per_seat = row.get("annual_cost_inr", 0) / total if total else 0
            wasted = per_seat * (total - active)
            findings.append({
                "type": "unused_licenses",
                "tool": row.get("tool_name", ""),
                "vendor": row.get("vendor", ""),
                "total_seats": total,
                "active_users": active,
                "unused_seats": total - active,
                "unused_pct": round(unused_pct, 1),
                "annual_cost": row.get("annual_cost_inr", 0),
                "annual_impact": wasted,
                "renewal_date": str(row.get("renewal_date", "")),
            })
    return findings


# ── SLA Anomalies ─────────────────────────────────────────────────────────────

def detect_sla_risks(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Flag tickets close to or exceeding their SLA deadline."""
    findings = []
    if df is None or df.empty:
        return findings
    for _, row in df.iterrows():
        sla_h = row.get("sla_hours", 0)
        elapsed_h = row.get("elapsed_hours", 0)
        if sla_h == 0:
            continue
        remaining = sla_h - elapsed_h
        pct_used = elapsed_h / sla_h * 100
        if pct_used >= 80:  # 80% of SLA elapsed
            findings.append({
                "type": "sla_breach_risk",
                "ticket_id": row.get("ticket_id", ""),
                "title": row.get("title", ""),
                "priority": row.get("priority", ""),
                "sla_hours": sla_h,
                "elapsed_hours": elapsed_h,
                "remaining_hours": max(0, remaining),
                "remaining_minutes": round(max(0, remaining) * 60),
                "pct_elapsed": round(pct_used, 1),
                "breached": elapsed_h >= sla_h,
                "penalty": row.get("estimated_penalty_inr", 0),
                "annual_impact": row.get("estimated_penalty_inr", 0),
                "customer": row.get("customer", ""),
            })
    return findings


# ── Invoice Anomalies ─────────────────────────────────────────────────────────

def detect_duplicate_invoices(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Find invoices with same number + vendor but multiple payments."""
    findings = []
    if df is None or df.empty or "vendor_name" not in df.columns or "invoice_number" not in df.columns or "amount_inr" not in df.columns:
        return findings
    grp = df.groupby(["vendor_name", "invoice_number"])
    for (vendor, inv_num), group in grp:
        if len(group) > 1:
            amount = group["amount_inr"].iloc[0]
            dup_count = len(group)
            findings.append({
                "type": "duplicate_invoice",
                "vendor": vendor,
                "invoice_number": inv_num,
                "occurrences": dup_count,
                "amount_per": amount,
                "total_paid": group["amount_inr"].sum(),
                "annual_impact": amount * (dup_count - 1),
                "department": group["department"].iloc[0],
            })
    return findings
