# App Flow — Revora

> Status: LOCKED — matches PRD.md core features.

## End-to-end flow (the "hero flow")

Razorpay webhook (or synthetic batch event)
│
▼

DETECT + DIAGNOSE
extract signals: failure_reason, amount, past_success_rate,
days_since_last_success, customer_ltv
compute deterministic risk score
Claude call → plain-language root-cause explanation (structured JSON)
│
▼
DECIDE + POLICY
expected-value calculation → candidate strategy
(retry / payment link / escalate to human / stop)
deterministic policy guardrails check:
max_retries? high-value → needs human approval? cooldown active?
if guardrail fails → action is BLOCKED, logged, case escalated
│
▼
EXECUTE
approved action sent via Razorpay adapter (real test-mode API for a
subset, simulator for batch scale)
every attempt (approved or blocked) written to the audit log
│
▼
MEASURE
outcome recorded (recovered / not recovered, amount, timestamp)
aggregated into batch-level recovery rate, baseline comparison,
cost-per-recovery
│
▼
Dashboard (risk queue, recovered ₹, audit trail)



## Dashboard user flow

1. Merchant logs in (single hardcoded login)
2. Lands on summary view: total at-risk ₹, recovered ₹ this batch,
   recovery rate vs. baseline, cost per recovery
3. Risk queue table: each case with status (pending / recovering /
   recovered / escalated / stopped), click into a case to see its full
   audit trail (signals → diagnosis → decision → policy check → action →
   outcome)
4. "Run batch" control (for the demo): triggers the pipeline across the
   synthetic dataset and refreshes the summary live

## Failure / edge-case flows

- **LLM call fails or times out** → fall back to a conservative
  rule-based explanation/action (never let the pipeline hang or crash the
  batch run) — log this explicitly, it becomes part of the "what broke"
  submission doc.
- **Razorpay API unreachable** → fall back to simulator for that case,
  flagged in the audit log as `simulated: true`.
- **Duplicate webhook delivery** → deduplicated by event ID before any
  processing (see `webhook_server.py`), returns `duplicate_ignored`, no
  double action.
- **Policy guardrail blocks an action** → case is not silently dropped; it
  moves to an "escalated / needs human review" state, visible in the
  dashboard risk queue, not hidden.