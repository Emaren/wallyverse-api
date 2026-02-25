# Wallyverse API

Minimal FastAPI service for Phase 0 launch:

- `POST /v1/waitlist`
- `GET /v1/stats`
- `GET /health`

## Local run

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Payload example

```json
{
  "email": "tamer@example.com",
  "source_page": "connect",
  "wants_shop_signals": true
}
```
