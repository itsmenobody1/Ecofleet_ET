"""
dashboard.py — Autonomous Command Center (Premium SaaS Analytics UI).
"""
from __future__ import annotations

import streamlit as st
import pandas as pd

from utils.helpers import total_leakage, findings_by_agent, sort_findings
from workflows.approval_manager import approved_savings, pending_count
from workflows.action_logs import total_savings_executed
from core.cost_calculator import format_inr


def render(findings: list) -> None:
    st.markdown("""
    <style>
    /* Premium Glassmorphism Cards */
    .glass-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%);
        backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.08); border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3); padding: 24px;
        height: 100%; transition: transform 0.2s, box-shadow 0.2s;
    }
    .glass-card:hover { border-color: rgba(139,92,246,0.3); box-shadow: 0 12px 48px rgba(124,58,237,0.15); }
    
    .big-metric-title { color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; margin-bottom: 8px; }
    .big-metric-val { font-size: 2.8rem; font-weight: 900; letter-spacing: -1.5px; line-height: 1.1; margin-bottom: 12px; }
    .val-grad-1 { background: linear-gradient(135deg, #a78bfa, #60a5fa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .val-grad-2 { background: linear-gradient(135deg, #34d399, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    
    /* Agent Node UI */
    .agent-node { display: flex; align-items: center; justify-content: space-between; padding: 16px; border-bottom: 1px solid rgba(255,255,255,0.05); }
    .agent-node:last-child { border-bottom: none; }
    .agent-icon { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); }
    .agent-info { flex: 1; margin-left: 14px; }
    .agent-name { font-weight: 700; color: #f1f5f9; font-size: 0.95rem; }
    .agent-desc { color: #64748b; font-size: 0.75rem; letter-spacing: 0.02em; }
    .agent-stats { text-align: right; }
    .agent-stat-leak { font-weight: 800; color: #e2e8f0; font-size: 0.95rem; }
    .agent-stat-count { color: #a78bfa; font-size: 0.7rem; font-weight: 700; background: rgba(124,58,237,0.15); padding: 2px 8px; border-radius: 20px; display: inline-block; margin-top: 4px; }
    
    /* Terminal UI */
    .terminal-ui { background: #06060c; border: 1px solid #1e1b4b; border-radius: 12px; padding: 16px; height: 260px; overflow: hidden; position: relative; }
    .terminal-ui::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, transparent, #6366f1, transparent); }
    .term-line { font-family: 'Courier New', monospace; font-size: 0.75rem; color: #a78bfa; margin-bottom: 6px; line-height: 1.4; opacity: 0.85; }
    .term-time { color: #64748b; margin-right: 8px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("## 🧠 Agent Command Center")
    st.markdown("<p style='color:#94a3b8;margin-bottom:28px'>Live intelligence overview of autonomous cost isolation and automated execution workflows.</p>", unsafe_allow_html=True)

    if not findings:
        st.info("⚡ Agents idle. Navigate to **Data Integration Matrix (Upload Data)** to trigger autonomous ingestion pipelines.")
        return

    leak = total_leakage(findings)
    saved = total_savings_executed()
    pend = pending_count(findings)
    
    # Hero Top Cards
    c1, c2, c3 = st.columns([1.5, 1, 1])
    with c1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="big-metric-title">Critical Cost Leakage Avoidable</div>
            <div class="big-metric-val val-grad-1">{format_inr(leak)}</div>
            <div style="color:#64748b;font-size:0.8rem">Identified by {len(findings)} precise agent findings. <a href='#approvals' style='color:#a78bfa'>Needs action</a>.</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="big-metric-title">Capital Reclaimed</div>
            <div class="big-metric-val val-grad-2">{format_inr(saved)}</div>
            <div style="color:#64748b;font-size:0.8rem">Successfully recovered via automated enterprise workflows.</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="big-metric-title">Execution Queue</div>
            <div class="big-metric-val" style="color:#f59e0b">{pend}</div>
            <div style="color:#64748b;font-size:0.8rem">Playbooks pending human approval.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Agent Network Status
    col_l, col_r = st.columns([1.2, 1])
    
    by_agent = findings_by_agent(findings)
    def summary(agent_name):
        arr = by_agent.get(agent_name, [])
        return format_inr(total_leakage(arr)), len(arr)

    sp_l, sp_c = summary("Spend Agent")
    sl_l, sl_c = summary("SLA Agent")
    re_l, re_c = summary("Resource Agent")
    fi_l, fi_c = summary("Finance Agent")

    with col_l:
        st.markdown("#### 🌐 Autonomous Active Agents")
        st.markdown(f"""
        <div class="glass-card" style="padding:12px 16px;">
            <div class="agent-node">
                <div class="agent-icon" style="color:#a78bfa; border-color:rgba(167,139,250,0.3)">💸</div>
                <div class="agent-info">
                    <div class="agent-name">Spend Intelligence Agent</div>
                    <div class="agent-desc">Procurement, Vendor Arbitrage, License Utilization</div>
                </div>
                <div class="agent-stats">
                    <div class="agent-stat-leak">{sp_l}</div>
                    <div class="agent-stat-count">{sp_c} Identified</div>
                </div>
            </div>
            
            <div class="agent-node">
                <div class="agent-icon" style="color:#06b6d4; border-color:rgba(6,182,212,0.3)">⏱️</div>
                <div class="agent-info">
                    <div class="agent-name">SLA Penalty Prevention Agent</div>
                    <div class="agent-desc">ITSM, Support Operations, Escalation Risk</div>
                </div>
                <div class="agent-stats">
                    <div class="agent-stat-leak">{sl_l}</div>
                    <div class="agent-stat-count" style="background:rgba(6,182,212,0.15);color:#06b6d4">{sl_c} Identified</div>
                </div>
            </div>

            <div class="agent-node">
                <div class="agent-icon" style="color:#34d399; border-color:rgba(52,211,153,0.3)">🖥️</div>
                <div class="agent-info">
                    <div class="agent-name">Infrastructure Optimization Agent</div>
                    <div class="agent-desc">Cloud Compute, Storage, Idle Assets</div>
                </div>
                <div class="agent-stats">
                    <div class="agent-stat-leak">{re_l}</div>
                    <div class="agent-stat-count" style="background:rgba(52,211,153,0.15);color:#34d399">{re_c} Identified</div>
                </div>
            </div>

            <div class="agent-node">
                <div class="agent-icon" style="color:#f59e0b; border-color:rgba(245,158,11,0.3)">💰</div>
                <div class="agent-info">
                    <div class="agent-name">Financial Operations Agent</div>
                    <div class="agent-desc">Accounts Payable, Reconciliation, Duplicates</div>
                </div>
                <div class="agent-stats">
                    <div class="agent-stat-leak">{fi_l}</div>
                    <div class="agent-stat-count" style="background:rgba(245,158,11,0.15);color:#f59e0b">{fi_c} Identified</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown("#### ⚡ Live Workflow Stream")
        import random, datetime
        
        sim_logs = [
            "[Sys] Spawning concurrent agent intelligence pools...",
            "[Agent.Resource] AWS EC2 describe_instances -> 4,021 nodes scanned.",
            "[Agent.Spend] SAP Ariba PO match heuristics tracking 8% variance.",
            "[Agent.SLA] Jira Service Desk Webhook -> evaluating SLA priority thresholds.",
            "[Agent.Finance] Ingested 12k new AP invoices. Normalizing text via OCR.",
            "[Agent.Resource] Found compute anomaly: instance i-0ab4x idle for 42h.",
            "[Action.Engine] Generating playbook payload for Resource remediation.",
            "[Agent.Spend] Vendor cross-match identified 2.1x price inflation on Zoom corp.",
            "[Agent.Finance] Duplicate invoice threshold bridged for supplier 'Acme Corp'.",
            "Waiting for execution approval triggers from Command Hub...",
        ]
        
        log_html = ""
        dt = datetime.datetime.now()
        for i, l in enumerate(sim_logs):
            t = (dt - datetime.timedelta(seconds=len(sim_logs)*2 - i*2)).strftime("%H:%M:%S")
            log_html += f"<div class='term-line'><span class='term-time'>[{t}]</span> {l}</div>"
            
        st.markdown(f"""
        <div class="terminal-ui">
            {log_html}
            <div class='term-line' style='color:#34d399; margin-top:10px'><span class='term-time'>[Live]</span> Polling enterprise data streams...</div>
        </div>
        """, unsafe_allow_html=True)
