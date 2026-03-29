"""
landing_page.py — Premium Dribbble-style SaaS landing page for ACIA.
"""
from __future__ import annotations
import streamlit as st


def render() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)
    _navbar()
    _hero()
    _trusted_by()
    _features()
    _analytics_showcase()
    _how_it_works()
    _cta_footer()


# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* Reset Streamlit chrome */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stAppViewContainer"] { padding: 0 !important; }
[data-testid="stVerticalBlock"] > div { padding: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none !important; }

* { box-sizing: border-box; font-family: 'Inter', sans-serif; scroll-behavior: smooth; }

/* ── Design tokens ───────────────────────────────────────────────── */
:root {
  --bg-deep:     #080816;
  --bg-dark:     #0d0b22;
  --bg-card:     rgba(255,255,255,0.04);
  --border:      rgba(255,255,255,0.08);
  --border-glow: rgba(139,92,246,0.35);
  --primary:     #7c3aed;
  --primary-l:   #a78bfa;
  --accent:      #06b6d4;
  --gold:        #f59e0b;
  --text-1:      #f1f5f9;
  --text-2:      #94a3b8;
  --text-3:      #475569;
  --radius-xl:   20px;
  --radius-2xl:  28px;
  --shadow-glow: 0 0 60px rgba(124,58,237,0.18);
}

/* ── Navbar ──────────────────────────────────────────────────────── */
.acia-nav {
  position: sticky; top: 0; z-index: 1000;
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 56px;
  background: rgba(8,8,22,0.72);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border);
}
.acia-nav-logo {
  font-size: 1.5rem; font-weight: 900; letter-spacing: -0.5px;
  background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  text-decoration: none;
}
.acia-nav-logo span { font-weight: 300; opacity: 0.7; font-size: 0.9rem; }
.acia-nav-links { display: flex; gap: 36px; }
.acia-nav-links a {
  color: var(--text-2); text-decoration: none; font-size: 0.9rem; font-weight: 500;
  transition: color .2s;
}
.acia-nav-links a:hover { color: var(--text-1); }
.acia-nav-cta {
  padding: 10px 24px; border-radius: 12px; font-weight: 700; font-size: 0.9rem;
  background: linear-gradient(135deg, #7c3aed, #6366f1);
  color: #fff; border: none; cursor: pointer;
  box-shadow: 0 4px 20px rgba(124,58,237,0.4);
  transition: transform .18s, box-shadow .18s;
  text-decoration: none; display: inline-block;
}
.acia-nav-cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(124,58,237,0.55);
}

/* ── Section base ────────────────────────────────────────────────── */
.section {
  width: 100%; padding: 96px 56px;
  position: relative; overflow: hidden;
}
.section-sm { padding: 64px 56px; }
.container { max-width: 1180px; margin: 0 auto; }

/* ── Hero ────────────────────────────────────────────────────────── */
.hero-section {
  min-height: 88vh;
  background: radial-gradient(ellipse 80% 60% at 50% -10%, rgba(124,58,237,0.28) 0%, transparent 70%),
              radial-gradient(ellipse 50% 40% at 90% 60%, rgba(6,182,212,0.14) 0%, transparent 60%),
              linear-gradient(180deg, #0d0b22 0%, #080816 100%);
  display: flex; align-items: center;
  padding: 80px 56px 96px;
}
.hero-inner {
  max-width: 1180px; margin: 0 auto; width: 100%;
  display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center;
}
.hero-badge {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 7px 16px; border-radius: 50px;
  background: rgba(124,58,237,0.15);
  border: 1px solid rgba(139,92,246,0.3);
  color: #a78bfa; font-size: 0.8rem; font-weight: 600;
  letter-spacing: 0.04em; text-transform: uppercase;
  margin-bottom: 24px;
}
.hero-badge-dot {
  width: 6px; height: 6px; border-radius: 50%; background: #a78bfa;
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.5; transform: scale(1.4); }
}
.hero-headline {
  font-size: 3.8rem; font-weight: 900; line-height: 1.1; letter-spacing: -1.5px;
  color: var(--text-1); margin: 0 0 20px;
}
.hero-headline .grad {
  background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 55%, #34d399 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub {
  font-size: 1.1rem; line-height: 1.7; color: var(--text-2); margin: 0 0 36px;
  max-width: 480px;
}
.hero-btns { display: flex; gap: 14px; flex-wrap: wrap; }
.btn-primary {
  padding: 15px 32px; border-radius: 14px; font-weight: 700; font-size: 1rem;
  background: linear-gradient(135deg, #7c3aed, #6366f1);
  color: #fff; border: none; cursor: pointer; text-decoration: none;
  box-shadow: 0 6px 28px rgba(124,58,237,0.5);
  transition: transform .18s, box-shadow .18s; display: inline-block;
}
.btn-primary:hover { transform: translateY(-3px); box-shadow: 0 12px 40px rgba(124,58,237,0.6); }
.btn-outline {
  padding: 15px 32px; border-radius: 14px; font-weight: 700; font-size: 1rem;
  background: transparent; color: var(--text-1); text-decoration: none;
  border: 1px solid rgba(255,255,255,0.15); cursor: pointer;
  backdrop-filter: blur(10px); display: inline-block;
  transition: border-color .18s, background .18s;
}
.btn-outline:hover { border-color: rgba(139,92,246,0.5); background: rgba(124,58,237,0.1); }

/* ── Dashboard Mockup Card ───────────────────────────────────────── */
.mockup-card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 24px;
  padding: 28px;
  backdrop-filter: blur(24px);
  box-shadow: 0 32px 80px rgba(0,0,0,0.5), 0 0 0 1px rgba(124,58,237,0.15);
  position: relative; overflow: hidden;
}
.mockup-card::before {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(ellipse 60% 40% at 70% 20%, rgba(124,58,237,0.12), transparent);
  pointer-events: none;
}
.mockup-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.mockup-title { font-weight: 700; font-size: 0.95rem; color: var(--text-1); }
.badge-live {
  display: flex; align-items: center; gap: 5px;
  font-size: 0.72rem; font-weight: 600; color: #34d399;
  background: rgba(52,211,153,0.12); border: 1px solid rgba(52,211,153,0.25);
  padding: 4px 10px; border-radius: 20px;
}
.badge-live-dot { width: 5px; height: 5px; border-radius: 50%; background: #34d399; animation: pulse 1.5s infinite; }
.mockup-big-metric {
  font-size: 2.4rem; font-weight: 900; color: #fff; letter-spacing: -1px; margin: 4px 0 20px;
}
.mockup-big-metric span { color: #a78bfa; }
.mockup-big-label { font-size: 0.78rem; color: var(--text-2); letter-spacing: 0.05em; text-transform: uppercase; }
.mini-metrics { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 18px; }
.mini-metric {
  background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px; padding: 12px 14px;
}
.mini-metric-val { font-size: 1.1rem; font-weight: 800; color: var(--text-1); }
.mini-metric-lbl { font-size: 0.68rem; color: var(--text-3); margin-top: 2px; text-transform: uppercase; letter-spacing: 0.04em; }
.bar-chart { display: flex; align-items: flex-end; gap: 6px; height: 60px; margin-top: 8px; }
.bar {
  flex: 1; border-radius: 4px 4px 0 0;
  background: linear-gradient(180deg, #a78bfa, #6366f1);
  opacity: 0.6; transition: opacity .2s;
}
.bar:hover { opacity: 1; }
.bar.accent { background: linear-gradient(180deg, #34d399, #06b6d4); }
.bar.gold   { background: linear-gradient(180deg, #fbbf24, #f59e0b); }
.agent-pills { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 12px; }
.agent-pill {
  font-size: 0.7rem; font-weight: 600; padding: 4px 10px; border-radius: 20px;
  border: 1px solid;
}

/* ── Trusted By ───────────────────────────────────────────────────── */
.trusted-section {
  background: #080816;
  padding: 48px 56px;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}
.trusted-label { text-align: center; color: var(--text-3); font-size: 0.78rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 28px; }
.logo-row { display: flex; justify-content: center; align-items: center; gap: 52px; flex-wrap: wrap; }
.logo-name { color: rgba(255,255,255,0.18); font-size: 1.3rem; font-weight: 800; letter-spacing: -0.5px; filter: grayscale(1); transition: all .2s; }
.logo-name:hover { color: rgba(255,255,255,0.45); }

/* ── Features ────────────────────────────────────────────────────── */
.features-section { background: #0d0b22; }
.section-tag { color: #a78bfa; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px; }
.section-headline {
  font-size: 2.8rem; font-weight: 900; letter-spacing: -1px; color: var(--text-1);
  margin: 0 0 12px;
}
.section-sub { color: var(--text-2); font-size: 1.05rem; line-height: 1.65; margin: 0 0 52px; max-width: 540px; }
.features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.feature-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 20px; padding: 32px 28px;
  transition: transform .22s, border-color .22s, box-shadow .22s;
  position: relative; overflow: hidden;
}
.feature-card::before {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(ellipse 80% 60% at 0% 0%, rgba(124,58,237,0.06), transparent);
}
.feature-card:hover {
  transform: translateY(-5px);
  border-color: rgba(139,92,246,0.3);
  box-shadow: 0 16px 48px rgba(124,58,237,0.18);
}
.feature-icon {
  width: 50px; height: 50px; border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.4rem; margin-bottom: 18px;
  background: rgba(124,58,237,0.15);
  border: 1px solid rgba(139,92,246,0.2);
}
.feature-title { font-size: 1.05rem; font-weight: 700; color: var(--text-1); margin: 0 0 8px; }
.feature-desc { font-size: 0.88rem; color: var(--text-2); line-height: 1.6; }

/* ── Analytics Section ────────────────────────────────────────────── */
.analytics-section {
  background: linear-gradient(135deg, #060614 0%, #0d0b22 60%, #06091a 100%);
  padding: 96px 56px;
}
.analytics-inner { display: grid; grid-template-columns: 1fr 1.2fr; gap: 72px; align-items: center; max-width: 1180px; margin: 0 auto; }
.analytics-big-num {
  font-size: 5rem; font-weight: 900; letter-spacing: -3px;
  background: linear-gradient(135deg, #a78bfa, #60a5fa);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  margin: 16px 0;
}
.analytics-points { list-style: none; padding: 0; margin: 24px 0 0; }
.analytics-points li {
  display: flex; align-items: flex-start; gap: 10px;
  color: var(--text-2); font-size: 0.95rem; padding: 10px 0;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}
.analytics-points li .check { color: #34d399; font-size: 1rem; margin-top: 1px; }
.analytics-visual {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 24px; padding: 28px;
  backdrop-filter: blur(16px);
  box-shadow: 0 40px 100px rgba(0,0,0,0.6);
}
.a-chart-row { display: flex; gap: 12px; margin-bottom: 12px; }
.a-mini { flex: 1; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07); border-radius: 14px; padding: 16px; }
.a-mini-val { font-size: 1.4rem; font-weight: 800; color: #fff; }
.a-mini-lbl { font-size: 0.68rem; color: var(--text-3); text-transform: uppercase; letter-spacing: 0.05em; margin-top: 3px; }
.a-mini.green .a-mini-val  { color: #34d399; }
.a-mini.purple .a-mini-val { color: #a78bfa; }
.a-chart-bars { display: flex; align-items: flex-end; gap: 6px; height: 90px; margin: 12px 0; padding: 0 4px; }
.a-bar { flex: 1; border-radius: 4px 4px 0 0; }
.a-bar.p  { background: linear-gradient(0deg, #4c1d95, #a78bfa); }
.a-bar.c  { background: linear-gradient(0deg, #0e7490, #22d3ee); }
.a-bar.g  { background: linear-gradient(0deg, #064e3b, #34d399); }
.a-bar-lbl { font-size: 0.62rem; color: var(--text-3); text-align: center; margin-top: 4px; }
.agent-rows { margin-top: 14px; }
.agent-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 9px 0; border-bottom: 1px solid rgba(255,255,255,0.05);
  font-size: 0.84rem;
}
.agent-row-name { color: var(--text-2); display: flex; align-items: center; gap: 8px; }
.agent-row-val  { color: var(--text-1); font-weight: 700; }
.agent-row-badge { font-size: 0.68rem; padding: 2px 8px; border-radius: 20px; font-weight: 600; }

/* ── How It Works ─────────────────────────────────────────────────── */
.how-section { background: #080816; }
.steps-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2px; position: relative; }
.steps-row::before {
  content: ''; position: absolute; top: 32px; left: 16%; right: 16%;
  height: 1px; background: linear-gradient(90deg, transparent, rgba(139,92,246,0.4), transparent);
}
.step {
  display: flex; flex-direction: column; align-items: center;
  text-align: center; padding: 0 28px;
}
.step-num {
  width: 64px; height: 64px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.4rem; font-weight: 900;
  background: linear-gradient(135deg, rgba(124,58,237,0.3), rgba(99,102,241,0.2));
  border: 2px solid rgba(139,92,246,0.4);
  color: #a78bfa; margin-bottom: 24px; position: relative; z-index: 1;
  backdrop-filter: blur(8px);
}
.step-title { font-size: 1.05rem; font-weight: 700; color: var(--text-1); margin: 0 0 10px; }
.step-desc  { font-size: 0.88rem; color: var(--text-2); line-height: 1.65; }

/* ── Footer ───────────────────────────────────────────────────────── */
.acia-footer {
  background: #060610;
  border-top: 1px solid var(--border);
  padding: 56px 56px 32px;
}
.footer-top { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 40px; margin-bottom: 48px; }
.footer-logo { font-size: 1.5rem; font-weight: 900; background: linear-gradient(135deg, #a78bfa, #60a5fa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px; }
.footer-tagline { color: var(--text-3); font-size: 0.84rem; line-height: 1.6; max-width: 260px; }
.footer-col-title { color: var(--text-1); font-weight: 700; font-size: 0.85rem; margin-bottom: 14px; }
.footer-links { list-style: none; padding: 0; margin: 0; }
.footer-links li { margin-bottom: 10px; }
.footer-links a { color: var(--text-3); text-decoration: none; font-size: 0.84rem; transition: color .2s; }
.footer-links a:hover { color: var(--text-2); }
.footer-bottom {
  display: flex; justify-content: space-between; align-items: center;
  padding-top: 24px; border-top: 1px solid var(--border);
  color: var(--text-3); font-size: 0.78rem;
}
.socials { display: flex; gap: 14px; }
.social-btn {
  width: 34px; height: 34px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);
  background: rgba(255,255,255,0.03); display: flex; align-items: center; justify-content: center;
  font-size: 0.9rem; cursor: pointer; transition: border-color .2s;
}
.social-btn:hover { border-color: rgba(139,92,246,0.4); }

/* ── CTA to enter app ────────────────────────────────────────────── */
.enter-app-btn {
  display: block; margin: 0 auto 40px;
  padding: 16px 40px; border-radius: 14px; font-weight: 800; font-size: 1.05rem;
  background: linear-gradient(135deg, #7c3aed, #6366f1);
  color: #fff; border: none; cursor: pointer;
  box-shadow: 0 8px 32px rgba(124,58,237,0.5);
  letter-spacing: 0.01em;
  transition: transform .18s, box-shadow .18s;
}
.enter-app-btn:hover { transform: translateY(-3px); box-shadow: 0 14px 48px rgba(124,58,237,0.65); }
</style>
"""


# ─────────────────────────────────────────────────────────────────────────────
# SECTIONS (Formatted with no indentation to avoid Markdown code blocks)
# ─────────────────────────────────────────────────────────────────────────────

def _navbar():
    html = """
<nav class="acia-nav">
<a href="#" class="acia-nav-logo">ACIA <span>| AI Cost Platform</span></a>
<div class="acia-nav-links">
<a href="#features">Features</a>
<a href="#analytics">Analytics</a>
<a href="#how-it-works">How it Works</a>
<a href="#launch">Launch App</a>
</div>
<a href="#launch" class="acia-nav-cta">Get Started</a>
</nav>
"""
    st.markdown(html, unsafe_allow_html=True)


def _hero():
    html = """
<section class="hero-section">
<div class="hero-inner">
<div>
<div class="hero-badge">
<div class="hero-badge-dot"></div>
AI-Powered Enterprise Cost Intelligence
</div>
<h1 class="hero-headline">
Turn Enterprise Data Into<br>
<span class="grad">Measurable Savings</span>
</h1>
<p class="hero-sub">
AI agents that detect cost leakage and take autonomous action
before money is lost — quantified in ₹, approved by you.
</p>
<div class="hero-btns">
<a href="#launch" class="btn-primary">🚀 Launch Platform</a>
<a href="#features" class="btn-outline">▶ Platform Features</a>
</div>
<p style="color:#475569;font-size:0.78rem;margin-top:18px;">
No credit card required &nbsp;·&nbsp; Works on your data in minutes
</p>
</div>
<div class="mockup-card">
<div class="mockup-header">
<span class="mockup-title">🧠 ACIA Intelligence Hub</span>
<span class="badge-live"><span class="badge-live-dot"></span>Live Analysis</span>
</div>
<div style="color:#94a3b8;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em">Monthly Savings Detected</div>
<div class="mockup-big-metric"><span>₹</span>12,43,800</div>
<div class="mini-metrics">
<div class="mini-metric">
<div class="mini-metric-val" style="color:#34d399">48</div>
<div class="mini-metric-lbl">Findings</div>
</div>
<div class="mini-metric">
<div class="mini-metric-val" style="color:#f59e0b">12</div>
<div class="mini-metric-lbl">Pending</div>
</div>
<div class="mini-metric">
<div class="mini-metric-val" style="color:#a78bfa">₹2.08 Cr</div>
<div class="mini-metric-lbl">Annual leak</div>
</div>
</div>
<div style="color:#475569;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:8px">Leakage by Agent</div>
<div class="bar-chart">
<div class="bar" style="height:75%"></div>
<div class="bar" style="height:55%"></div>
<div class="bar accent" style="height:38%"></div>
<div class="bar gold" style="height:62%"></div>
<div class="bar" style="height:80%"></div>
<div class="bar accent" style="height:45%"></div>
<div class="bar" style="height:90%"></div>
<div class="bar gold" style="height:30%"></div>
</div>
<div class="agent-pills" style="margin-top:14px">
<span class="agent-pill" style="color:#a78bfa;border-color:rgba(167,139,250,0.3);background:rgba(124,58,237,0.1)">💸 Spend Agent</span>
<span class="agent-pill" style="color:#f59e0b;border-color:rgba(245,158,11,0.3);background:rgba(245,158,11,0.08)">⏱️ SLA Agent</span>
<span class="agent-pill" style="color:#34d399;border-color:rgba(52,211,153,0.3);background:rgba(52,211,153,0.08)">🖥️ Resource</span>
<span class="agent-pill" style="color:#60a5fa;border-color:rgba(96,165,250,0.3);background:rgba(59,130,246,0.08)">💰 Finance</span>
</div>
</div>
</div>
</section>
"""
    st.markdown(html, unsafe_allow_html=True)


def _trusted_by():
    html = """
<section class="trusted-section">
<div class="trusted-label">Trusted by enterprise teams globally</div>
<div class="logo-row">
<span class="logo-name">Infosys</span>
<span class="logo-name">Wipro</span>
<span class="logo-name">TCS</span>
<span class="logo-name">HCL</span>
<span class="logo-name">Reliance</span>
<span class="logo-name">Adani</span>
<span class="logo-name">Mahindra</span>
</div>
</section>
"""
    st.markdown(html, unsafe_allow_html=True)


def _features():
    html = """
<section id="features" class="section features-section">
<div class="container">
<div class="section-tag">✦ Platform Capabilities</div>
<h2 class="section-headline">Six agents.<br>One mission: save ₹.</h2>
<p class="section-sub">Every agent is purpose-built to detect a specific class of enterprise cost leakage — automatically.</p>
<div class="features-grid">
<div class="feature-card">
<div class="feature-icon">💸</div>
<div class="feature-title">Spend Intelligence</div>
<div class="feature-desc">Detects price overruns, duplicate vendor sourcing, and inflated procurement costs in real time.</div>
</div>
<div class="feature-card">
<div class="feature-icon">⏱️</div>
<div class="feature-title">SLA Breach Prevention</div>
<div class="feature-desc">Monitors ticket SLAs 24/7 and escalates at-risk issues before penalty exposure crystallises.</div>
</div>
<div class="feature-card">
<div class="feature-icon">🖥️</div>
<div class="feature-title">Resource Optimization</div>
<div class="feature-desc">Flags idle cloud servers and over-provisioned infra, scheduling shutdowns with one-click approval.</div>
</div>
<div class="feature-card">
<div class="feature-icon">💰</div>
<div class="feature-title">Financial Reconciliation</div>
<div class="feature-desc">Catches duplicate invoices, unauthorized spend, and billing anomalies in your AP ledger.</div>
</div>
<div class="feature-card">
<div class="feature-icon">🤖</div>
<div class="feature-title">Autonomous Workflows</div>
<div class="feature-desc">Findings flow into an approval pipeline. You approve once — ACIA executes the action.</div>
</div>
<div class="feature-card">
<div class="feature-icon">📊</div>
<div class="feature-title">Quantified Cost Impact</div>
<div class="feature-desc">Every finding is backed by precise ₹ math — no vague alerts, only actionable numbers.</div>
</div>
</div>
</div>
</section>
"""
    st.markdown(html, unsafe_allow_html=True)


def _analytics_showcase():
    html = """
<section id="analytics" class="analytics-section">
<div class="analytics-inner">
<div>
<div class="section-tag">✦ Deep Analytics</div>
<h2 class="section-headline" style="font-size:2.4rem">
Real numbers.<br>Real savings.
</h2>
<div class="analytics-big-num">₹2.08 Cr</div>
<p style="color:#94a3b8;font-size:0.95rem">
Detected in a single enterprise scan across procurement, cloud, SaaS, and AP invoices.
</p>
<ul class="analytics-points">
<li><span class="check">✔</span> Every saving is quantified before action is taken</li>
<li><span class="check">✔</span> Root-cause explanation with step-by-step cost math</li>
<li><span class="check">✔</span> Automated playbook for each finding type</li>
<li><span class="check">✔</span> Full audit trail of every action executed</li>
</ul>
</div>
<div class="analytics-visual">
<div style="color:#94a3b8;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:14px">Savings Breakdown</div>
<div class="a-chart-row">
<div class="a-mini purple">
<div class="a-mini-val">₹98.4L</div>
<div class="a-mini-lbl">Spend Agent</div>
</div>
<div class="a-mini green">
<div class="a-mini-val">₹72L</div>
<div class="a-mini-lbl">Resource Agent</div>
</div>
</div>
<div class="a-chart-row">
<div class="a-mini" style="">
<div class="a-mini-val" style="color:#f59e0b">₹23.5L</div>
<div class="a-mini-lbl">Finance Agent</div>
</div>
<div class="a-mini" style="">
<div class="a-mini-val" style="color:#06b6d4">₹14.9L</div>
<div class="a-mini-lbl">SLA Agent</div>
</div>
</div>
<div style="color:#475569;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.06em;margin:16px 0 4px">Monthly trend</div>
<div class="a-chart-bars">
<div style="display:flex;flex-direction:column;align-items:center;flex:1">
<div class="a-bar p" style="height:40%;width:100%"></div>
<div class="a-bar-lbl">Jan</div>
</div>
<div style="display:flex;flex-direction:column;align-items:center;flex:1">
<div class="a-bar c" style="height:55%;width:100%"></div>
<div class="a-bar-lbl">Feb</div>
</div>
<div style="display:flex;flex-direction:column;align-items:center;flex:1">
<div class="a-bar g" style="height:72%;width:100%"></div>
<div class="a-bar-lbl">Mar</div>
</div>
<div style="display:flex;flex-direction:column;align-items:center;flex:1">
<div class="a-bar p" style="height:88%;width:100%"></div>
<div class="a-bar-lbl">Apr</div>
</div>
<div style="display:flex;flex-direction:column;align-items:center;flex:1">
<div class="a-bar c" style="height:65%;width:100%"></div>
<div class="a-bar-lbl">May</div>
</div>
<div style="display:flex;flex-direction:column;align-items:center;flex:1">
<div class="a-bar g" style="height:95%;width:100%"></div>
<div class="a-bar-lbl">Jun</div>
</div>
</div>
<div class="agent-rows">
<div class="agent-row">
<span class="agent-row-name">💸 Spend Agent</span>
<span class="agent-row-val">₹98.4L<span style="margin-left:8px" class="agent-row-badge" style="color:#a78bfa;background:rgba(167,139,250,0.1);border:1px solid rgba(167,139,250,0.25)">25 findings</span></span>
</div>
<div class="agent-row">
<span class="agent-row-name">🖥️ Resource Agent</span>
<span class="agent-row-val">₹72L <span style="margin-left:8px" class="agent-row-badge">11 findings</span></span>
</div>
<div class="agent-row">
<span class="agent-row-name">💰 Finance Agent</span>
<span class="agent-row-val">₹23.5L <span style="margin-left:8px" class="agent-row-badge">5 findings</span></span>
</div>
<div class="agent-row">
<span class="agent-row-name">⏱️ SLA Agent</span>
<span class="agent-row-val">₹14.9L <span style="margin-left:8px" class="agent-row-badge">7 findings</span></span>
</div>
</div>
</div>
</div>
</section>
"""
    st.markdown(html, unsafe_allow_html=True)


def _how_it_works():
    html = """
<section id="how-it-works" class="section how-section">
<div class="container" style="text-align:center">
<div class="section-tag" style="text-align:center">✦ How It Works</div>
<h2 class="section-headline" style="margin-bottom:14px">Three steps to ₹ savings</h2>
<p class="section-sub" style="margin:0 auto 60px;text-align:center">
ACIA works end-to-end — from raw enterprise CSV to executed savings in minutes.
</p>
<div class="steps-row">
<div class="step">
<div class="step-num">1</div>
<div class="step-title">Connect Enterprise Data</div>
<div class="step-desc">Upload procurement, cloud usage, SaaS licences, tickets, or AP invoices as CSV — or use our sample datasets.</div>
</div>
<div class="step">
<div class="step-num">2</div>
<div class="step-title">AI Detects Cost Inefficiencies</div>
<div class="step-desc">Four autonomous agents scan every row, cross-reference benchmarks, quantify the ₹ impact, and explain their reasoning.</div>
</div>
<div class="step">
<div class="step-num">3</div>
<div class="step-title">Approve Actions, Save Money</div>
<div class="step-desc">Review findings in the approvals queue, click Approve once — ACIA triggers the corrective action and logs savings.</div>
</div>
</div>
</div>
</section>
"""
    st.markdown(html, unsafe_allow_html=True)


def _cta_footer():
    # Enter App CTA
    st.markdown("""
    <div id="launch" style="background:linear-gradient(135deg,rgba(124,58,237,0.15),rgba(99,102,241,0.1));
         border:1px solid rgba(139,92,246,0.3);border-radius:24px;padding:52px;
         max-width:780px;margin:80px auto 40px;text-align:center;">
      <div style="font-size:2rem;font-weight:900;color:#f1f5f9;letter-spacing:-0.5px;margin-bottom:10px">
        Ready to stop the leakage?
      </div>
      <div style="color:#94a3b8;font-size:1rem;margin-bottom:28px">
        Upload your enterprise data and get your first ₹ finding in under 30 seconds.
      </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns([1, 2, 1])
    with cols[1]:
        if st.button("🚀 Launch ACIA Dashboard →", type="primary", use_container_width=True,
                     key="landing_enter_app"):
            st.session_state["current_page"] = "🏠 Dashboard"
            st.session_state["skip_landing"] = True
            st.rerun()

    html = """
<footer class="acia-footer">
<div class="footer-top">
<div>
<div class="footer-logo">ACIA</div>
<div class="footer-tagline">Autonomous Cost Intelligence Agent — turning enterprise data into measurable ₹ savings.</div>
</div>
<div>
<div class="footer-col-title">Product</div>
<ul class="footer-links">
<li><a href="#features">Features</a></li>
<li><a href="#analytics">Analytics</a></li>
<li><a href="#how-it-works">How it Works</a></li>
<li><a href="#launch">Launch App</a></li>
</ul>
</div>
<div>
<div class="footer-col-title">Resources</div>
<ul class="footer-links">
<li><a href="#">Documentation</a></li>
<li><a href="#">API Reference</a></li>
<li><a href="#">Case Studies</a></li>
</ul>
</div>
<div>
<div class="footer-col-title">Company</div>
<ul class="footer-links">
<li><a href="#">About</a></li>
<li><a href="#">Privacy Policy</a></li>
<li><a href="#">Terms of Service</a></li>
</ul>
</div>
</div>
<div class="footer-bottom">
<span>© 2026 ACIA Technologies. All rights reserved.</span>
<div class="socials">
<div class="social-btn">𝕏</div>
<div class="social-btn">in</div>
<div class="social-btn">gh</div>
<div class="social-btn">✉</div>
</div>
</div>
</footer>
"""
    st.markdown(html, unsafe_allow_html=True)
