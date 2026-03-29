"""
findings_page.py — "Show The Math" Intelligence Hub displaying AI logic transparently.
"""
from __future__ import annotations

import streamlit as st

from utils.helpers import sort_findings, total_leakage
from utils.constants import SEVERITY_COLORS, AGENT_INFO
from core.cost_calculator import format_inr, severity_emoji
from llm.reasoning import enrich_finding

_AGENT_ICONS = {a: v["icon"] for a, v in AGENT_INFO.items()}


def render(findings: list) -> None:
    st.markdown("""
    <style>
    .finding-card {
        background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px; padding: 24px; margin-bottom: 20px;
        backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 4px 24px rgba(0,0,0,0.2); transition: transform 0.2s, border-color 0.2s;
    }
    .finding-card:hover { border-color: rgba(139,92,246,0.4); transform: translateY(-2px); }
    
    .fc-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; }
    .fc-title-row { display: flex; align-items: center; gap: 12px; }
    .fc-title { font-weight: 800; color: #f1f5f9; font-size: 1.15rem; letter-spacing: -0.5px; }
    .fc-badge { padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
    .fc-impact { text-align: right; }
    .fc-impact-val { font-size: 1.4rem; font-weight: 900; }
    .fc-impact-lbl { font-size: 0.7rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px; }
    
    .fc-desc { color: #94a3b8; font-size: 0.95rem; line-height: 1.6; margin-bottom: 24px; }
    
    .fc-math-box { background: #06060c; border: 1px solid #1e1b4b; border-radius: 12px; padding: 16px; font-family: 'Courier New', monospace; color: #a78bfa; font-size: 0.85rem; margin-top: 12px; }
    .fc-math-title { font-family: 'Inter', sans-serif; font-size: 0.7rem; color: #64748b; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 8px; }
    .math-step { padding: 4px 0; border-bottom: 1px dashed rgba(139,92,246,0.2); }
    .math-step:last-child { border-bottom: none; }
    
    .fc-playbook { background: rgba(52,211,153,0.05); border-left: 3px solid #34d399; padding: 16px; border-radius: 0 12px 12px 0; margin-top: 12px; }
    .fc-playbook-title { font-size: 0.75rem; color: #34d399; text-transform: uppercase; font-weight: 800; letter-spacing: 0.05em; margin-bottom: 8px; }
    .fc-playbook-step { color: #e2e8f0; font-size: 0.85rem; padding: 4px 0; display: flex; align-items: flex-start; gap: 8px; }
    .fc-playbook-check { color: #34d399; font-weight: bold; margin-top: -2px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("## 🔍 Deep Intelligence Hub")
    st.markdown("<p style='color:#94a3b8;margin-bottom:32px'>Transparent AI analysis revealing exact quantifiable cost derivations and execution playbooks.</p>", unsafe_allow_html=True)

    if not findings:
        st.info("⚡ Agent engine idle. No findings resident in active memory.")
        return

    filtered = sort_findings(findings, "annual_impact")
    
    for i, f in enumerate(filtered):
        sev   = f.get("severity", "LOW")
        emoji = severity_emoji(sev)
        color = SEVERITY_COLORS.get(sev, "#6b7280")
        agent_icon = _AGENT_ICONS.get(f.get("agent", ""), "🤖")
        
        # Enrich dynamically using the LLM for deep contextual explanations and specific math
        enriched_key = f"rich_{i}"
        if enriched_key not in st.session_state:
            with st.spinner("🤖 Translating raw tensors into explainable math..."):
                st.session_state[enriched_key] = enrich_finding(f)
                
        rich = st.session_state[enriched_key]
        
        # Build visually structured math
        raw_math = rich.get("cost_math", "Calculated automatically by agent parameters.")
        math_lines = raw_math.split('\n')
        math_html = "".join([f"<div class='math-step'>{line.strip()}</div>" for line in math_lines if line.strip()])
        
        # Build playbooks
        pb = rich.get("playbook", ["Initiate default remediation."])
        pb_html = "".join([f"<div class='fc-playbook-step'><span class='fc-playbook-check'>✓</span> {step}</div>" for step in pb])
        
        title = f.get('title', 'Cost Anomaly')
        desc = f.get('description', '')
        impact = f.get('formatted_impact', '0')
        agent = f.get('agent', 'Generic')

        # Card render
        st.markdown(f"""
        <div class="finding-card">
            <div class="fc-header">
                <div class="fc-title-row">
                    <span style="font-size:1.6rem">{emoji}</span>
                    <div>
                        <div class="fc-title">{title}</div>
                        <div style="margin-top:4px"><span class="fc-badge" style="background:rgba(255,255,255,0.06);color:#94a3b8">{agent_icon} {agent}</span></div>
                    </div>
                </div>
                <div class="fc-impact">
                    <div class="fc-impact-val" style="color:{color}">{impact}</div>
                    <div class="fc-impact-lbl">Avoidable Leakage / yr</div>
                </div>
            </div>
            
            <div class="fc-desc">{desc}</div>
            
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px">
                <div>
                    <div class="fc-math-title">💹 Quantifiable Cost Math</div>
                    <div class="fc-math-box">{math_html}</div>
                </div>
                <div>
                    <div class="fc-playbook">
                        <div class="fc-playbook-title">Autonomous Action Playbook</div>
                        {pb_html}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action button exactly below card
        col1, col2 = st.columns([1, 4])
        with col1:
             if st.button("🚀 Queue for Execution", key=f"q_{i}", type="primary"):
                 if "pending_approvals" not in st.session_state: st.session_state.pending_approvals = set()
                 st.session_state.pending_approvals.add(i)
                 st.success("Target loaded into Execution Queue.")
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
