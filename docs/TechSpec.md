# Tech Spec — Revora

> Status: LOCKED — matches PRD.md decisions. Update here first if the stack changes.

## Tech Stack
- **Backend:** Python + FastAPI (thin layer — mostly plain functions, not
  heavy class hierarchies; speed over architecture purity for a 4-day build)
- **Storage:** SQLite (single file, zero setup — see Schema.md for tables)
- **Dashboard:** Streamlit (fastest path to a working UI; not React)
- **LLM:** Claude API — structured JSON output for reasoning/explanation
  only (never for policy/execution decisions — see Rules.md)
- **Payments:** Razorpay test-mode REST API — Subscriptions, Webhooks,
  Payment Links (via `pipeline/razorpay_client.py` adapter)

## External APIs Used

| API | Purpose | Docs |
|---|---|---|
| Razorpay Subscriptions | Create/fetch subscriptions, simulate charges | https://razorpay.com/docs/api/payments/subscriptions/ |
| Razorpay Webhooks | Receive `subscription.pending`, `subscription.charged`, `payment.failed` events | https://razorpay.com/docs/webhooks/ |
| Razorpay Payment Links | Send a recovery payment link as one strategy option | https://razorpay.com/docs/payment-links/ |
| Claude API (Messages) | Root-cause explanation + structured reasoning output | https://docs.claude.com/en/docs/build-with-claude/tool-use/overview |

> Rule: verify each endpoint against current docs before implementing —
> don't rely on memory (see Rules.md #2).

## Authentication

- **Razorpay:** server-side API key auth only (Key ID + Secret in `.env`,
  never exposed to the dashboard/frontend)
- **Dashboard:** single hardcoded merchant login — a plain username/password
  check against an env var or a one-row `users` table, setting a signed
  session cookie via FastAPI (or Streamlit's session state if the whole
  dashboard stays in Streamlit — decide during Day 1, see PRD Open
  Questions #3). Not production-grade auth; explicitly out of scope per
  PRD Non-Goals.

## Database

- SQLite, single file (`revora.db`), accessed via Python's built-in
  `sqlite3` (no ORM needed at this scale — keeps it simple to debug live
  during the demo).
- See `Schema.md` for tables and relationships.
- Why SQLite over Postgres: zero setup/hosting, trivial to reset between
  test runs, and the entire batch (300–500 rows) fits comfortably —
  Postgres would add setup risk for no benefit at this scale.

## Known Constraints (fill in as discovered during Day 0/1)
- Razorpay test-mode subsequent debit only works within 3 days of card
  token creation (per Razorpay docs) — relevant if testing spans multiple
  days.
- LLM call failure/latency: every LLM call in the pipeline needs a
  fallback (e.g., default to a conservative rule-based explanation/action
  if the Claude API call errors or times out) — do not let a single LLM
  failure crash the batch run.