import uuid
from typing import Dict


class InMemoryStore:
    def __init__(self) -> None:
        self.sessions: Dict[str, Dict] = {}

    def start(self) -> str:
        sid = str(uuid.uuid4())
        self.sessions[sid] = {"answers": {}}
        return sid

    def answer(self, session_id: str, question_id: str, score: float) -> None:
        self.sessions.setdefault(session_id, {"answers": {}})
        self.sessions[session_id]["answers"][question_id] = float(score)

    def get_answers(self, session_id: str) -> Dict[str, float]:
        return dict(self.sessions.get(session_id, {}).get("answers", {}))

STORE = InMemoryStore()

