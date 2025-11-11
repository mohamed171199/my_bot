from typing import List, Protocol


class ChatProvider(Protocol):
    async def generate(self, system_prompt: str, message: str, history: List[dict]) -> str:
        ...

