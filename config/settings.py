import os
import json
from typing import Any, Dict


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
DATA_DIR = os.path.join(BASE_DIR, "data")


def get_system_prompt() -> str:
    path = os.path.join(CONFIG_DIR, "system_prompt.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""


def get_starters() -> Dict[str, Any]:
    path = os.path.join(DATA_DIR, "conversation_starters.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # fallback
    return {
        "starters": [
            {"label": "ابدأ الخطة الرقمية للمصنع"},
            {"label": "كيف أقيّم النضج الرقمي؟"},
            {"label": "ارسم لي خارطة الطريق"},
        ]
    }

