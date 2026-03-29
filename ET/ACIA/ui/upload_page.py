"""
upload_page.py — Premium Data Integration Hub for ACIA's autonomous agents.
"""
from __future__ import annotations

import streamlit as st
import time

from core.data_loader import load_sample_data, load_uploaded_data
from utils.constants import DATASET_LABELS
import agents.spend_agent as spend_agent
import agents.sla_agent as sla_agent
import agents.resource_agent as resource_agent
import agents.finance_agent as finance_agent


def render() -> None:
    st.markdown("""
    <style>
    .integration-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
    .int-card {
        background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px; padding: 20px; text-align: center;
        transition: all 0.3s ease; box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        backdrop-filter: blur(12px);
    }
    .int-card:hover { transform: translateY(-3px); border-color: rgba(167,139,250,0.4); box-shadow: 0 8px 30px rgba(124,58,237,0.15); }
    .int-icon { font-size: 2.2rem; margin-bottom: 12px; }
    .int-title { font-weight: 700; color: #f1f5f9; font-size: 0.95rem; }
    .int-status { font-size: 0.7rem; color: #34d399; font-weight: 600; text-transform: uppercase; margin-top: 6px; letter-spacing: 0.05em; }
    .status-dot { display: inline-block; width: 6px; height: 6px; background: #34d399; border-radius: 50%; margin-right: 4px; animation: pulse 2s infinite; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("## 🔌 Data Integration Matrix")
    st.markdown("<p style='color:#94a3b8; font-size:0.95rem; margin-bottom:24px'>Connect ACIA to your enterprise infrastructure. Agents continuously ingest data to detect structural cost anomalies in real-time.</p>", unsafe_allow_html=True)

    # Simulated Live Integrations UI
    st.markdown("""
    <div class="integration-grid">
        <div class="int-card"><div class="int-icon">☁️</div><div class="int-title">AWS Cost Explorer</div><div class="int-status"><span class="status-dot"></span>Connected</div></div>
        <div class="int-card"><div class="int-icon">🎫</div><div class="int-title">Jira Service Desk</div><div class="int-status"><span class="status-dot"></span>Connected</div></div>
        <div class="int-card"><div class="int-icon">📦</div><div class="int-title">SAP Ariba</div><div class="int-status"><span class="status-dot"></span>Connected</div></div>
        <div class="int-card"><div class="int-icon">🔑</div><div class="int-title">Okta SSO</div><div class="int-status"><span class="status-dot"></span>Connected</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Tabs for execution simulation
    tab_sample, tab_upload = st.tabs(["🚀 Sync Live Systems (Simulate)", "📁 Manual CSV Override"])

    with tab_sample:
        st.markdown("<div style='padding:10px 0'>Trigger an immediate agent sync across all connected enterprise platforms.</div>", unsafe_allow_html=True)
        if st.button("⚡ Trigger Autonomous Agent Sync", type="primary", use_container_width=True):
            _run_analysis_pipeline()

    with tab_upload:
        st.info("Manually upload CSV data dumps for offline or air-gapped agent analysis.")
        uploaded_map = {}
        cols = st.columns(2)
        idx = 0
        for ds in DATASET_LABELS:
            with cols[idx % 2]:
                f = st.file_uploader(f"{DATASET_LABELS[ds]} CSV", type=["csv"], key=f"up_{ds}")
                if f: uploaded_map[ds] = f.read()
            idx += 1

        if uploaded_map:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⚡ Run Analytics on Uploaded Files", type="primary", use_container_width=True):
                _run_analysis_pipeline(uploaded_map)


def _run_analysis_pipeline(uploaded_map: dict = None) -> None:
    st.markdown("---")
    st.markdown("### 🧠 Agent Execution Pipeline")

    dfs = {}
    with st.spinner("Ingesting enterprise data streams..."):
        time.sleep(1)
        for ds in DATASET_LABELS:
            if uploaded_map and ds in uploaded_map:
                dfs[ds] = load_uploaded_data(uploaded_map[ds], ds)
            else:
                dfs[ds] = load_sample_data(ds)

    st.success("✅ Data streams ingested and normalized (Procurement, Cloud, SaaS, ITSM, Invoices).")
    
    # Progress UI
    progress_bar = st.progress(0)
    status_text = st.empty()
    terminal_box = st.empty()
    
    logs = []
    def log(msg: str):
        logs.append(msg)
        terminal_box.markdown(f"<div style='background:#0d0b22;border:1px solid #1e1b4b;padding:12px;border-radius:8px;font-family:monospace;color:#a78bfa;font-size:0.8rem;height:120px;overflow-y:auto'>{'<br>'.join(logs)}</div>", unsafe_allow_html=True)

    all_findings = []

    # Spend Agent
    status_text.markdown("**⚡ Spend Intelligence Agent running...**")
    log("[Spend Agent] Cross-referencing vendor pricing vs global market index...")
    time.sleep(0.8)
    sp_f = spend_agent.run(procurement_df=dfs.get("procurement"), saas_df=dfs.get("saas_usage"))
    all_findings.extend(sp_f)
    log(f"[Spend Agent] Detected {len(sp_f)} procurement anomalies.")
    progress_bar.progress(25)

    # SLA Agent
    status_text.markdown("**⚡ SLA Penalty Prevention Agent running...**")
    log("[SLA Agent] Parsing structured ticket metadata and escalation boundaries...")
    time.sleep(0.8)
    sla_f = sla_agent.run(tickets_df=dfs.get("tickets"))
    all_findings.extend(sla_f)
    log(f"[SLA Agent] Flagged {len(sla_f)} SLA risk vectors.")
    progress_bar.progress(50)

    # Resource Agent
    status_text.markdown("**⚡ Infrastructure Optimization Agent running...**")
    log("[Resource Agent] Scanning AWS utilization thresholds and idle heuristics...")
    time.sleep(0.8)
    res_f = resource_agent.run(cloud_df=dfs.get("cloud_usage"))
    all_findings.extend(res_f)
    log(f"[Resource Agent] Identified {len(res_f)} stranded cloud assets.")
    progress_bar.progress(75)

    # Finance Agent
    status_text.markdown("**⚡ Financial Ops Agent running...**")
    log("[Finance Agent] Reconciling Accounts Payable ledgers for duplicate vectors...")
    time.sleep(0.8)
    fin_f = finance_agent.run(invoices_df=dfs.get("invoices"))
    all_findings.extend(fin_f)
    log(f"[Finance Agent] Surfaced {len(fin_f)} AP discrepancies.")
    progress_bar.progress(100)
    
    status_text.empty()

    st.session_state.findings = all_findings
    st.session_state.dataframes = dfs
    st.session_state.approvals = {}

    from utils.helpers import total_leakage
    from core.cost_calculator import format_inr
    leak = total_leakage(all_findings)

    st.balloons()
    st.markdown(f"""
    <div style='background:linear-gradient(135deg, rgba(167,139,250,0.1), rgba(99,102,241,0.1));
                border:1px solid rgba(139,92,246,0.3); border-radius:16px; padding:24px; text-align:center;
                box-shadow: 0 8px 32px rgba(124,58,237,0.15)'>
        <h2 style='margin:0;color:#f1f5f9;font-weight:900'>Pipeline Complete</h2>
        <div style='color:#a78bfa;font-size:1.4rem;font-weight:800;margin:12px 0'>{format_inr(leak)} / yr Avoidable Cost Identified</div>
        <p style='color:#94a3b8;font-size:0.9rem;margin:0'>{len(all_findings)} actionable findings pushed to intelligence hub.</p>
    </div>
    """, unsafe_allow_html=True)
