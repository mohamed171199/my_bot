Setup

- Create a virtualenv and install `requirements.txt`.
- Optionally copy `.env.example` to `.env` and set provider env vars.
- Run `uvicorn my_bot.app:app --reload`.

SIRI Assessment (experimental)

- Open `http://127.0.0.1:8000/static/siri.html` to run a demo assessment.
- Questions and dimensions are defined at:
  - `my_bot/siri/config/dimensions.json:1`
  - `my_bot/siri/config/questions.json:1`
- API endpoints:
  - `POST /siri/start` → `{ session_id, total_questions }`
  - `GET /siri/questions` → list of questions
  - `POST /siri/answer` → `{ session_id, question_id, score }`
  - `GET /siri/result?session_id=...` → overall/pillar/dimension scores + recommendations

Notes: Provided configs are placeholders for demonstration. Replace with your SIRI-aligned content.

Import starters from your JSON

- Keep the file `GTE_Conversation_Starters_Complete.json.JSON` in the project root.
- Run `python my_bot/scripts/clean_gte_json.py` to extract conversation starters into `my_bot/data/conversation_starters.json`.

Switch providers

- Default is `echo` (local, offline).
- To use OpenAI: set `PROVIDER=openai`, `OPENAI_API_KEY`, and optionally `OPENAI_MODEL`.

Web UI

- Open `http://127.0.0.1:8000/` for ATLAM Arabic chat interface with starters.
