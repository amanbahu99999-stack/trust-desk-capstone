# TrustDesk demo script (about 3 minutes)

1. Start the service with `python3 app.py`, then open `http://localhost:8000`.
2. Open **T-001**, click **Triage**, then **Generate cited draft**. Point out the `KB-REFUND-001` citation.
3. Click **Recommend refund review**. Explain that the action is only `pending_approval`.
4. Click **Approve action**. Show that it becomes `executed`; repeat the recommendation to explain the idempotency key prevents a duplicate action.
5. Open **T-003** and generate a draft. Show that the identity-bypass/prompt-injection request is blocked and escalated.
6. Click **Run evaluation suite**. Highlight the triage accuracy, citation coverage, and unsafe-action blocking results.
7. Close by showing `GET /api/traces` or describing the stored trace record for every triage, draft, and action.
