# Implementation Plan

Deadline: 5 Sept. Locked scope — no re-architecture past this point.

## Day 0 (1 Sept) — Verify + Lock — DONE
- Repo created, skeleton pushed
- Razorpay test-mode POC (plan/customer/subscription/webhook)

## Day 1 (2 Sept) — Data + Detect/Diagnose
- Synthetic data generator (300–500 events)
- Signal extraction (risk score, failure reason, history)
- LLM root-cause explanation (structured JSON)

## Day 2 (3 Sept) — Decide+Policy + Execute
- Strategy selection (retry / payment link / escalate / stop)
- Deterministic policy guardrails (max retries, amount threshold, human approval)
- Razorpay adapter calls (subset real, rest simulated) + audit logging

## Day 3 (4 Sept) — Measure + Dashboard
- Outcome tracking, full batch run
- Baseline vs AI-system comparison (headline number)
- Streamlit dashboard: risk queue, recovered ₹, recovery rate, audit trail
- One deliberate failure-case handled gracefully

## Day 4 (5 Sept) — Buffer + Submit
- Golden-path seeded demo (no live-API flakiness during pitch)
- README + "what broke and how you recovered" doc
- 5-min pitch video
- Public repo finalized, submit with buffer
