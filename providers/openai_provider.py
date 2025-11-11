import os
from typing import List
import httpx


class OpenAIProvider:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not set")

    async def generate(self, system_prompt: str, message: str, history: List[dict]) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        for turn in history:
            role = turn.get("role", "user")
            content = turn.get("content", "")
            messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": message})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"model": self.model, "messages": messages}

        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
            return data["choices"][0]["message"]["content"].strip()

