"""
settings.py — Central configuration for ACIA.
Override via .env or environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── LLM ──────────────────────────────────────────────────────────────────────
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))

# Whether to use LLM enrichment or fall back to rule-based summaries
USE_LLM: bool = bool(OPENAI_API_KEY)

# ── Currency ──────────────────────────────────────────────────────────────────
CURRENCY_SYMBOL: str = "₹"
CURRENCY_CODE: str = "INR"

# ── Anomaly Thresholds ────────────────────────────────────────────────────────
IDLE_CPU_THRESHOLD: float = float(os.getenv("IDLE_CPU_THRESHOLD", "5.0"))   # %
IDLE_MEMORY_THRESHOLD: float = float(os.getenv("IDLE_MEMORY_THRESHOLD", "10.0"))  # %
SLA_BREACH_MINUTES: int = int(os.getenv("SLA_BREACH_MINUTES", "60"))
DUPLICATE_INVOICE_TOLERANCE: float = float(os.getenv("DUPLICATE_INVOICE_TOLERANCE", "0.01"))
PRICE_DIFF_THRESHOLD_PCT: float = float(os.getenv("PRICE_DIFF_THRESHOLD_PCT", "10.0"))  # %
UNUSED_SEAT_THRESHOLD_PCT: float = float(os.getenv("UNUSED_SEAT_THRESHOLD_PCT", "20.0"))  # %

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_DATA_DIR: str = os.path.join(BASE_DIR, "data", "sample_data")
UPLOADS_DIR: str = os.path.join(BASE_DIR, "data", "uploads")
ACTION_LOG_PATH: str = os.path.join(BASE_DIR, "data", "action_log.jsonl")
