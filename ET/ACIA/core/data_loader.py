"""
data_loader.py — Load, validate, and normalise enterprise CSV data.
"""
from __future__ import annotations

import os
import io
import pandas as pd
from typing import Optional
from config.settings import SAMPLE_DATA_DIR


EXPECTED_COLUMNS = {
    "procurement": ["vendor_id", "vendor_name", "item_description", "unit_price_inr",
                    "quantity", "total_inr", "contract_price_inr", "market_price_inr",
                    "purchase_date", "category"],
    "cloud_usage": ["server_id", "server_name", "region", "instance_type",
                    "cpu_usage_pct", "memory_usage_pct", "monthly_cost_inr",
                    "last_active", "environment"],
    "saas_usage":  ["license_id", "tool_name", "vendor", "plan", "total_seats",
                    "active_users", "monthly_cost_inr", "annual_cost_inr",
                    "renewal_date", "department"],
    "tickets":     ["ticket_id", "title", "priority", "status", "created_at",
                    "sla_hours", "elapsed_hours", "estimated_penalty_inr"],
    "invoices":    ["invoice_id", "vendor_name", "invoice_number", "invoice_date",
                    "amount_inr", "department", "status", "description"],
}


def load_sample_data(dataset: str) -> pd.DataFrame:
    """Load a named sample dataset from data/sample_data/."""
    path = os.path.join(SAMPLE_DATA_DIR, f"{dataset}.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Sample dataset not found: {path}")
    return _read_and_clean(pd.read_csv(path), dataset)


def load_uploaded_data(file_bytes: bytes, dataset_name: str) -> pd.DataFrame:
    """Load a user-uploaded CSV given raw bytes."""
    df = pd.read_csv(io.BytesIO(file_bytes))
    return _read_and_clean(df, dataset_name)


def _read_and_clean(df: pd.DataFrame, dataset: str) -> pd.DataFrame:
    """Lowercase columns, strip whitespace, parse dates."""
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Parse date-like columns
    for col in df.columns:
        if "date" in col or col in ("created_at", "last_active"):
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
            except Exception:
                pass

    # Numeric coercion for _inr and _pct columns
    for col in df.columns:
        if col.endswith("_inr") or col.endswith("_pct") or col.endswith("_hours") \
                or col in ("quantity", "total_seats", "active_users", "elapsed_hours", "sla_hours"):
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def get_dataset_summary(df: pd.DataFrame) -> dict:
    """Return a quick summary dict for UI display."""
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "null_counts": df.isnull().sum().to_dict(),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
    }
