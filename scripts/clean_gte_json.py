import json
import os
import re
from typing import Optional


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SOURCE_FILE = os.path.join(ROOT, "GTE_Conversation_Starters_Complete.json.JSON")
TARGET_FILE = os.path.join(ROOT, "my_bot", "data", "conversation_starters.json")


def strip_js_comments(text: str) -> str:
    # remove // ... comments
    text = re.sub(r"(^|\s)//.*$", "", text, flags=re.MULTILINE)
    # remove /* ... */ comments
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    return text


def try_fix_trailing_commas(text: str) -> str:
    # naive removal of trailing commas before ] or }
    text = re.sub(r",(\s*[\]\}])", r"\1", text)
    return text


def load_source() -> Optional[dict]:
    if not os.path.exists(SOURCE_FILE):
        return None
    with open(SOURCE_FILE, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()
    cleaned = try_fix_trailing_commas(strip_js_comments(raw))
    try:
        return json.loads(cleaned)
    except Exception:
        return None


def extract_starters(data: dict) -> dict:
    # Try to find any list-like under keys that look like starters
    # Fallback to empty if unknown structure
    candidates = []
    def walk(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (list, tuple)) and ("starter" in k.lower() or "prompts" in k.lower() or "starters" in k.lower()):
                    candidates.append(v)
                walk(v)
        elif isinstance(obj, list):
            for x in obj:
                walk(x)
    walk(data)

    labels = []
    for arr in candidates:
        for item in arr:
            if isinstance(item, str):
                labels.append({"label": item})
            elif isinstance(item, dict):
                label = item.get("label") or item.get("text") or item.get("title")
                if isinstance(label, str) and label.strip():
                    labels.append({"label": label.strip()})
    if not labels:
        labels = [{"label": "ابدأ تقييم التحول الرقمي للمصنع"}]
    return {"starters": labels}


def main():
    data = load_source()
    if not data:
        print("Source JSON not found or unreadable; keeping default starters.")
        return
    starters = extract_starters(data)
    os.makedirs(os.path.dirname(TARGET_FILE), exist_ok=True)
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        json.dump(starters, f, ensure_ascii=False, indent=2)
    print(f"Saved starters to {TARGET_FILE}")


if __name__ == "__main__":
    main()

