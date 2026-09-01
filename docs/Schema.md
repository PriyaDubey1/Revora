# Schema

> STATUS: TEMPLATE — fill during Day 1 (Detect/Diagnose stage build).

## Tables (draft — refine as built)

### `events` (raw incoming failure signals)
<!-- id, subscription_id, customer_id, amount, failure_reason, occurred_at, raw_payload -->

### `cases` (one row per at-risk revenue case being tracked)
<!-- id, event_id (FK), risk_score, diagnosis, recommended_action, status -->

### `actions` (every action attempted — the audit trail)
<!-- id, case_id (FK), action_type, policy_check_result, executed_at, result -->

### `outcomes` (measured results)
<!-- id, case_id (FK), recovered_amount, recovered_at, baseline_would_have_recovered -->

## Relationships
<!-- events 1:1 cases, cases 1:many actions, cases 1:1 outcomes -->
