"""
llm_client.py — LLM wrapper supporting OpenAI (and graceful fallback).
"""
from __future__ import annotations

import json
from typing import Any, Dict, Optional

from config.settings import OPENAI_API_KEY, LLM_MODEL, LLM_TEMPERATURE, USE_LLM
from config.prompts import SYSTEM_PROMPT

try:
    from openai import OpenAI
    _client = OpenAI(api_key=OPENAI_API_KEY) if USE_LLM else None
except ImportError:
    _client = None


def chat_completion(user_prompt: str, system_prompt: str = SYSTEM_PROMPT,
                    json_mode: bool = True) -> Optional[str]:
    """
    Call the LLM and return the raw text response.
    Returns None if LLM is unavailable.
    """
    if not USE_LLM or _client is None:
        return None

    try:
        kwargs: Dict[str, Any] = {
            "model": LLM_MODEL,
            "temperature": LLM_TEMPERATURE,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        response = _client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    except Exception as e:
        return None


def parse_json_response(raw: Optional[str]) -> Optional[Dict]:
    """Parse LLM JSON response safely."""
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None
