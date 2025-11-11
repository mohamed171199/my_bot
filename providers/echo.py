from typing import List


class EchoProvider:
    async def generate(self, system_prompt: str, message: str, history: List[dict]) -> str:
        prefix = "[ATLAM]"
        return f"{prefix} {message}"
