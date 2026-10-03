# TrustDesk - AI Support Operations Agent

TrustDesk is a local-first AI support operations demo. It turns support tickets into policy-grounded drafts, recommends sensitive actions without executing them, and stores auditable traces. It is intentionally deterministic so the complete assessment flow runs without a paid model API key.

## Run locally

```bash
python3 app.py
```

Open `http://localhost:8000`. The demo API token is `demo-support-token`.

## Run with Docker

```bash
docker build -t trustdesk .
docker run --rm -p 8000:8000 -v trustdesk-data:/app/data trustdesk
```

## Included workflow

1. `GET /api/tickets` and `GET /api/tickets/{id}` expose ticket context.
2. `POST /api/triage` returns intent, priority, and escalation decision.
3. `POST /api/drafts` retrieves trusted policy documents and returns a cited draft.
4. `POST /api/actions/refund-review` creates an approval-pending action using an idempotency key.
5. `POST /api/actions/{id}/approve` is the only path that executes the action.
6. `GET /api/traces` shows concise run traces; `POST /api/evals/run` runs seeded evaluation cases.

Every API route requires `Authorization: Bearer demo-support-token` except `/health` and the local UI.

### Example API request

```bash
curl -X POST http://localhost:8000/api/drafts \
  -H 'Authorization: Bearer demo-support-token' \
  -H 'Content-Type: application/json' \
  -d '{"ticket_id":"T-001"}'
```

## Safety design

- Ticket content is untrusted. Prompt-injection and identity-bypass patterns are blocked and escalated.
- The deliberately unsafe `KB-ADVERSARIAL-001` is marked untrusted and excluded from retrieval.
- Sensitive actions require a server-side approval record and idempotency key.
- The model behavior is deterministic for a reproducible, provider-free demo. Replace `triage`, `retrieve`, and `make_draft` with a provider adapter for production.

## Test

```bash
python3 -m unittest -v
```

## Demo

Use [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for a concise, under-five-minute recording plan. The intended walkthrough covers triage, cited drafting, approval-gated action execution, adversarial-input blocking, evaluations, and traces.

## Known limitations

This capstone uses local SQLite, keyword retrieval, and deterministic AI decisions to keep the demo reproducible. A production implementation would replace these with a managed database, hybrid/vector retrieval, authenticated user roles, encrypted secrets, asynchronous jobs, and a real model provider adapter.
