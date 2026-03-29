"""
app.py — ACIA Streamlit entry point, page router, and premium global theme.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ACIA — Autonomous Cost Intelligence Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state init ────────────────────────────────────────────────────────
if "findings"      not in st.session_state: st.session_state.findings      = []
if "dataframes"    not in st.session_state: st.session_state.dataframes    = {}
if "skip_landing"  not in st.session_state: st.session_state.skip_landing  = False
if "current_page"  not in st.session_state: st.session_state.current_page  = "🏠 Dashboard"

# ── Show landing page first unless user has entered the app ───────────────────
if not st.session_state.skip_landing:
    from ui import landing_page
    landing_page.render()
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# PREMIUM GLOBAL CSS (applied after landing)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {
  --bg-deep:   #080816;
  --bg-mid:    #0d0b22;
  --primary:   #7c3aed;
  --primary-l: #a78bfa;
  --accent:    #06b6d4;
  --text-1:    #f1f5f9;
  --text-2:    #94a3b8;
  --text-3:    #475569;
  --border:    rgba(255,255,255,0.07);
  --border-hi: rgba(139,92,246,0.35);
  --radius:    16px;
  --radius-xl: 22px;
}

html, body, [data-testid="stApp"] {
  background: #080816 !important;
  font-family: 'Inter', sans-serif !important;
  color: #f1f5f9 !important;
}

/* ── App Margins & Layout ── */
[data-testid="stAppViewContainer"] {
  padding: 0 !important;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stHeader"] {background: transparent !important;}
.block-container {
  padding: 2rem 4% !important;
  padding-top: 0 !important;
  max-width: 100% !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0d0b22 0%, #080816 100%) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* ── Radio nav items ── */
[data-testid="stSidebar"] .stRadio > label {
  color: #94a3b8 !important;
  font-size: 0.88rem !important;
  font-weight: 500 !important;
}
[data-testid="stSidebar"] .stRadio [aria-checked="true"] {
  color: #a78bfa !important;
  font-weight: 700 !important;
}

/* ── Buttons ── */
.stButton > button {
  border-radius: 12px !important;
  font-weight: 700 !important;
  font-family: 'Inter', sans-serif !important;
  transition: all 0.2s ease !important;
  letter-spacing: 0.01em !important;
  font-size: 0.9rem !important;
}
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #7c3aed, #6366f1) !important;
  border: none !important;
  color: #fff !important;
  box-shadow: 0 4px 20px rgba(99,102,241,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 32px rgba(99,102,241,0.5) !important;
}
.stButton > button[kind="secondary"] {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  color: #e2e8f0 !important;
}
.stButton > button[kind="secondary"]:hover {
  background: rgba(255,255,255,0.08) !important;
  border-color: rgba(139,92,246,0.35) !important;
}

/* ── Expanders ── */
div[data-testid="stExpander"] {
  background: rgba(255,255,255,0.025) !important;
  border: 1px solid rgba(255,255,255,0.07) !important;
  border-radius: 16px !important;
  margin-bottom: 10px !important;
  backdrop-filter: blur(12px) !important;
  transition: border-color .2s !important;
}
div[data-testid="stExpander"]:hover {
  border-color: rgba(139,92,246,0.25) !important;
}
.stExpander > details > summary {
  font-weight: 600 !important;
  font-size: 0.95rem !important;
  padding: 14px 18px !important;
}

/* ── Metrics ── */
[data-testid="stMetricValue"] {
  font-weight: 800 !important;
  font-size: 1.5rem !important;
  letter-spacing: -0.5px !important;
  color: #f1f5f9 !important;
}
[data-testid="stMetricLabel"] {
  color: #64748b !important;
  font-size: 0.78rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.06em !important;
  font-weight: 600 !important;
}
[data-testid="stMetricDelta"] { font-size: 0.82rem !important; }

/* ── Metric container card ── */
[data-testid="metric-container"] {
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,255,255,0.07) !important;
  border-radius: 16px !important;
  padding: 16px 20px 14px !important;
}

/* ── Inputs ── */
.stTextInput input, .stSelectbox select,
.stMultiSelect [data-baseweb="select"] > div {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 10px !important;
  color: #e2e8f0 !important;
  font-family: 'Inter', sans-serif !important;
}

/* ── Alerts ── */
div[data-testid="stAlert"] {
  border-radius: 12px !important;
  border-left-width: 3px !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: rgba(255,255,255,0.03) !important;
  border-radius: 12px !important;
  padding: 4px !important;
  border: 1px solid rgba(255,255,255,0.07) !important;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 8px !important;
  color: #94a3b8 !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  padding: 8px 18px !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, rgba(124,58,237,0.3), rgba(99,102,241,0.2)) !important;
  color: #e2e8f0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(139,92,246,0.5); }

/* ── Code blocks ── */
.stCode, code { background: rgba(255,255,255,0.04) !important; border-radius: 8px !important; }

/* ── Dividers ── */
hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #7c3aed !important; }

/* ── Checkbox ── */
.stCheckbox label { color: #94a3b8 !important; font-size: 0.9rem !important; }

/* ── Radio ── */
.stRadio label { color: #94a3b8 !important; font-size: 0.9rem !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
  background: rgba(255,255,255,0.02) !important;
  border: 1px dashed rgba(139,92,246,0.3) !important;
  border-radius: 14px !important;
}

/* ── Page headings ── */
h1, h2, h3 {
  font-family: 'Inter', sans-serif !important;
  letter-spacing: -0.5px !important;
  color: #f1f5f9 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Internal App CSS (top-bar navigation) ────────────────────────────────────
st.markdown("""
<style>
.app-topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 4%;
  padding-left: 60px; /* Space for the sidebar toggle arrow */
  background: rgba(8,8,22,0.85);
  border-bottom: 1px solid rgba(139,92,246,0.3);
  box-shadow: 0 4px 30px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05);
  backdrop-filter: blur(24px);
  position: sticky; top: 0; z-index: 100;
  margin: 0 -4% 2rem !important;
}
.app-logo {
  font-size: 1.25rem; font-weight: 900; letter-spacing: -0.5px;
  background: linear-gradient(135deg, #a78bfa, #60a5fa);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.app-logo sub { font-size: 0.7rem; font-weight: 400; color: #475569; -webkit-text-fill-color: #475569; margin-left: 4px; }
.app-badge {
  display: flex; align-items: center; gap: 5px;
  font-size: 0.72rem; font-weight: 600; color: #34d399;
  background: rgba(52,211,153,0.1); border: 1px solid rgba(52,211,153,0.25);
  padding: 4px 10px; border-radius: 20px;
}
.app-dot { width: 5px; height: 5px; border-radius: 50%; background: #34d399;
  animation: pulse 1.5s infinite; }
@keyframes pulse {
  0%,100% { opacity:1; transform:scale(1); }
  50%      { opacity:.5; transform:scale(1.4); }
}

/* ── Footer ── */
.app-footer {
  margin: 60px -4% 0;
  padding: 32px 4%;
  background: rgba(6,6,16,0.95);
  border-top: 1px solid rgba(255,255,255,0.05);
  display: flex; justify-content: space-between; align-items: center;
  color: #64748b; font-size: 0.85rem;
}
.app-footer .footer-logo { font-weight: 800; color: #a78bfa; letter-spacing: -0.5px; }
.app-footer-links { display: flex; gap: 24px; }
.app-footer-links a { color: #94a3b8; text-decoration: none; transition: color 0.2s; }
.app-footer-links a:hover { color: #f1f5f9; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1.2rem 0 0.8rem'>
        <div style='font-size:2.6rem;margin-bottom:4px'>🧠</div>
        <div style='font-size:1.4rem;font-weight:900;letter-spacing:-0.5px;
             background:linear-gradient(135deg,#a78bfa,#60a5fa);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent'>
            ACIA
        </div>
        <div style='color:#475569;font-size:0.72rem;margin-top:2px;font-weight:500'>
            Cost Intelligence Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div style='height:1px;background:linear-gradient(90deg,transparent,rgba(139,92,246,0.4),transparent);margin:8px 0 16px'></div>""", unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "📤 Upload Data", "🔍 AI Findings",
         "✅ Approvals", "📜 Action Logs"],
        index=["🏠 Dashboard", "📤 Upload Data", "🔍 AI Findings",
               "✅ Approvals", "📜 Action Logs"].index(
                   st.session_state.get("current_page", "🏠 Dashboard")),
        label_visibility="collapsed",
    )
    st.session_state["current_page"] = page

    # ── Quick stats ───────────────────────────────────────────────────────────
    findings = st.session_state.findings
    if findings:
        from utils.helpers import total_leakage
        from core.cost_calculator import format_inr
        from workflows.approval_manager import pending_count

        leak = total_leakage(findings)
        pend = pending_count(findings)

        st.markdown("""<div style='height:1px;background:rgba(255,255,255,0.06);margin:12px 0'></div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='padding:12px 8px'>
          <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px'>
            <span style='color:#64748b;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;font-weight:600'>Findings</span>
            <span style='color:#f1f5f9;font-weight:800;font-size:1rem'>{len(findings)}</span>
          </div>
          <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px'>
            <span style='color:#64748b;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;font-weight:600'>Leakage</span>
            <span style='color:#a78bfa;font-weight:800;font-size:0.95rem'>{format_inr(leak)}/yr</span>
          </div>
          <div style='display:flex;justify-content:space-between;align-items:center'>
            <span style='color:#64748b;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;font-weight:600'>Pending</span>
            <span style='background:rgba(245,158,11,0.15);color:#f59e0b;border:1px solid rgba(245,158,11,0.3);
                  border-radius:20px;padding:2px 10px;font-size:0.75rem;font-weight:700'>{pend}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""<div style='height:1px;background:rgba(255,255,255,0.06);margin:4px 0 12px'></div>""", unsafe_allow_html=True)

    if st.button("← Back to Landing", key="back_landing", use_container_width=True):
        st.session_state.skip_landing = False
        st.rerun()

    st.markdown("""
    <div style='color:#334155;font-size:0.68rem;text-align:center;padding:12px 8px 0;line-height:1.5'>
        ACIA doesn't show dashboards.<br>
        It finds ₹ leaks and acts.
    </div>
    """, unsafe_allow_html=True)

# ── Page top-bar ──────────────────────────────────────────────────────────────
findings = st.session_state.findings
has_findings = len(findings) > 0

page_info = {
    "🏠 Dashboard":   ("📊 Cost Intelligence Overview", "#a78bfa"),
    "📤 Upload Data": ("📤 Upload & Analyse",           "#60a5fa"),
    "🔍 AI Findings": ("🔍 AI Findings Feed",            "#34d399"),
    "✅ Approvals":   ("✅ Approval Workflow",            "#f59e0b"),
    "📜 Action Logs": ("📜 Action Logs",                  "#a78bfa"),
}
pi = page_info.get(page, (page, "#a78bfa"))

if has_findings:
    from utils.helpers import total_leakage
    from core.cost_calculator import format_inr
    badge_html = f"""<span class='app-badge'><span class='app-dot'></span>{format_inr(total_leakage(findings))}/yr detected</span>"""
else:
    badge_html = "<span class='app-badge' style='color:#64748b;background:rgba(100,116,139,0.1);border-color:rgba(100,116,139,0.2)'><span class='app-dot' style='background:#64748b'></span>No data loaded</span>"

st.markdown(f"""
<div class="app-topbar">
  <span class="app-logo">ACIA <sub>| {pi[0]}</sub></span>
  {badge_html}
</div>
""", unsafe_allow_html=True)
st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ── Page routing ──────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    from ui import dashboard
    dashboard.render(findings)

elif page == "📤 Upload Data":
    from ui import upload_page
    upload_page.render()

elif page == "🔍 AI Findings":
    from ui import findings_page
    findings_page.render(findings)

elif page == "✅ Approvals":
    from ui import approvals_page
    approvals_page.render(findings)

elif page == "📜 Action Logs":
    from ui import logs_page
    logs_page.render()

# ── Universal App Footer ────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
  <div>
    <span class="footer-logo">ACIA</span> &copy; 2026 Technologies. All rights reserved.
  </div>
  <div class="app-footer-links">
    <a href="#">Privacy</a>
    <a href="#">Terms</a>
    <a href="#">Support</a>
  </div>
</div>
""", unsafe_allow_html=True)
