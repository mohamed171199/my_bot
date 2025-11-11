from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
import os
import json

from .config.settings import get_system_prompt, get_starters
from .providers.echo import EchoProvider

try:
    from .providers.openai_provider import OpenAIProvider  # optional
except Exception:
    OpenAIProvider = None  # type: ignore


def get_provider():
    provider = os.getenv("PROVIDER", "echo").lower()
    if provider == "openai" and OpenAIProvider is not None:
        return OpenAIProvider()
    return EchoProvider()


app = FastAPI(title="ATLAM")
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")


@app.get("/")
async def root() -> HTMLResponse:
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(content=html)


@app.get("/starters")
async def starters() -> JSONResponse:
    return JSONResponse(get_starters())


@app.post("/chat")
async def chat(body: dict) -> JSONResponse:
    message: str = body.get("message", "").strip()
    history: List[dict] = body.get("history", [])
    if not message:
        return JSONResponse({"reply": ""})

    provider = get_provider()
    system_prompt = get_system_prompt()
    reply = await provider.generate(system_prompt=system_prompt, message=message, history=history)
    return JSONResponse({"reply": reply})


# For local dev: uvicorn my_bot.app:app --reload

# =============== SIRI Assessment API ===============
from .siri.models import StartResponse, SubmitAnswer
from .siri.store import STORE
from .siri.scoring import compute_scores


def _load_siri_dimensions():
    path = os.path.join(os.path.dirname(__file__), "siri", "config", "dimensions.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    from .siri.models import Dimension
    return [Dimension(**d) for d in data["dimensions"]]


def _load_siri_questions():
    path = os.path.join(os.path.dirname(__file__), "siri", "config", "questions.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    from .siri.models import Question, Option
    questions = []
    for q in data["questions"]:
        q["options"] = [Option(**o) for o in q.get("options", [])]
        questions.append(Question(**q))
    return questions


@app.post("/siri/start", response_model=StartResponse)
async def siri_start():
    sid = STORE.start()
    questions = _load_siri_questions()
    return StartResponse(session_id=sid, total_questions=len(questions))


@app.get("/siri/questions")
async def siri_questions():
    qs = _load_siri_questions()
    return JSONResponse([q.model_dump() for q in qs])


@app.post("/siri/answer")
async def siri_answer(payload: SubmitAnswer):
    STORE.answer(payload.session_id, payload.question_id, payload.score)
    return {"ok": True}


@app.get("/siri/result")
async def siri_result(session_id: str):
    answers = STORE.get_answers(session_id)
    dims = _load_siri_dimensions()
    qs = _load_siri_questions()
    res = compute_scores(answers, qs, dims)
    res.session_id = session_id
    return JSONResponse(res.model_dump())
