"""
approval_manager.py — Approval state management for findings.
"""
from __future__ import annotations

import streamlit as st
from typing import List, Dict, Any


def init_approvals(findings: List[Dict[str, Any]]) -> None:
    """Initialise approval state in session_state if not already set."""
    if "approvals" not in st.session_state:
        st.session_state.approvals = {}

    for i, f in enumerate(findings):
        key = _key(i, f)
        if key not in st.session_state.approvals:
            st.session_state.approvals[key] = "pending"


def get_approval_status(idx: int, finding: Dict) -> str:
    """Return 'pending' | 'approved' | 'rejected'."""
    return st.session_state.approvals.get(_key(idx, finding), "pending")


def set_approval_status(idx: int, finding: Dict, status: str) -> None:
    st.session_state.approvals[_key(idx, finding)] = status


def pending_count(findings: List[Dict]) -> int:
    return sum(1 for i, f in enumerate(findings)
               if get_approval_status(i, f) == "pending")


def approved_savings(findings: List[Dict]) -> float:
    return sum(
        f.get("annual_impact", 0)
        for i, f in enumerate(findings)
        if get_approval_status(i, f) == "approved"
    )


def _key(idx: int, finding: Dict) -> str:
    return f"finding_{idx}_{finding.get('type', '')}_{finding.get('title', '')[:30]}"
