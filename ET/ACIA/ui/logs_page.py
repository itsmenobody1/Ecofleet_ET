"""
logs_page.py — Action history log with savings timeline.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from workflows.action_logs import read_action_logs, clear_action_logs, total_savings_executed
from core.cost_calculator import format_inr


def render() -> None:
    st.markdown("## 📜 Action Logs")

    logs = read_action_logs()
    total_saved = total_savings_executed()

    # ── Header metrics ────────────────────────────────────────────────────────
    m1, m2, m3 = st.columns(3)
    m1.metric("🏆 Total Actions", len(logs))
    m2.metric("💚 Total Savings Executed", format_inr(total_saved))
    if logs:
        m3.metric("🕐 Latest Action", logs[0].get("executed_at", "")[:16].replace("T", " "))

    st.markdown("---")

    if not logs:
        st.info("No actions have been executed yet. Approve findings on the **Approvals** page.")
        return

    # ── Savings over Time chart ───────────────────────────────────────────────
    df = pd.DataFrame(logs)
    df["executed_at"] = pd.to_datetime(df["executed_at"], errors="coerce")
    df["annual_savings"] = pd.to_numeric(df.get("annual_savings", 0), errors="coerce").fillna(0)
    df_sorted = df.sort_values("executed_at")
    df_sorted["cumulative_savings"] = df_sorted["annual_savings"].cumsum()

    st.markdown("#### 📈 Cumulative Savings Executed")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_sorted["executed_at"],
        y=df_sorted["cumulative_savings"],
        mode="lines+markers",
        line=dict(color="#6366f1", width=3),
        marker=dict(size=8, color="#a78bfa"),
        fill="tozeroy",
        fillcolor="rgba(99,102,241,0.1)",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        margin=dict(l=0, r=0, t=10, b=0),
        height=220,
        xaxis=dict(showgrid=False, title=""),
        yaxis=dict(showgrid=True, gridcolor="rgba(99,102,241,0.1)", title="₹"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Log List ──────────────────────────────────────────────────────────────
    st.markdown("#### ⚡ Executed Actions")

    _CATEGORY_COLORS = {
        "Cloud Infrastructure": "#8b5cf6",
        "SaaS":       "#10b981",
        "Procurement": "#f59e0b",
        "Finance":    "#ef4444",
        "SLA":        "#3b82f6",
        "General":    "#6b7280",
    }

    for log in logs:
        cat   = log.get("category", "General")
        color = _CATEGORY_COLORS.get(cat, "#6b7280")
        ts    = log.get("executed_at", "")[:16].replace("T", " ")
        saved = log.get("annual_savings", 0)
        icon  = log.get("icon", "⚡")
        desc  = log.get("description", "Action executed.")
        by    = log.get("approved_by", "System")

        st.markdown(
            f"<div style='background:rgba(30,27,75,0.5);border-left:4px solid {color};"
            f"border-radius:0 8px 8px 0;padding:10px 16px;margin-bottom:8px'>"
            f"<span style='color:#94a3b8;font-size:0.78rem'>{ts} &nbsp;|&nbsp; "
            f"<b style='color:{color}'>{cat}</b> &nbsp;|&nbsp; By: {by}</span><br>"
            f"{icon} {desc}<br>"
            f"<span style='color:#10b981;font-weight:600'>💚 Saves {format_inr(saved)}/year</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    # ── Clear Logs ────────────────────────────────────────────────────────────
    st.markdown("---")
    if st.button("🗑️ Clear Action Logs (Demo Reset)", type="secondary"):
        clear_action_logs()
        st.rerun()
