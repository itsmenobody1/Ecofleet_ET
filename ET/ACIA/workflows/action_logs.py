"""
action_logs.py — Append-only JSONL action log for executed actions.
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Dict, Any, List

from config.settings import ACTION_LOG_PATH


def append_action_log(action: Dict[str, Any]) -> None:
    """Append a single action record to the JSONL log file."""
    os.makedirs(os.path.dirname(ACTION_LOG_PATH), exist_ok=True)
    action.setdefault("logged_at", datetime.now().isoformat())
    with open(ACTION_LOG_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(action, default=str) + "\n")


def read_action_logs() -> List[Dict[str, Any]]:
    """Read all action logs. Returns empty list if file doesn't exist."""
    if not os.path.exists(ACTION_LOG_PATH):
        return []
    logs = []
    with open(ACTION_LOG_PATH, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return list(reversed(logs))  # newest first


def clear_action_logs() -> None:
    """Clear all action logs (for demo reset)."""
    if os.path.exists(ACTION_LOG_PATH):
        os.remove(ACTION_LOG_PATH)


def total_savings_executed() -> float:
    """Sum all annual_savings from executed actions."""
    return sum(entry.get("annual_savings", 0) for entry in read_action_logs())
