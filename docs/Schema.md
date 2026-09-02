# Schema — Revora

> Status: LOCKED draft — refine field types during Day 1 build, don't
> restructure tables without updating this file first.

## Tables

### `events` — raw incoming failure signals
| Column | Type | Notes |
|---|---|---|
| id | TEXT PK | UUID |
| subscription_id | TEXT | Razorpay subscription ID (or synthetic ID) |
| customer_id | TEXT | Razorpay customer ID (or synthetic ID) |
| amount | INTEGER | paise |
| failure_reason | TEXT | e.g. insufficient_funds, expired_card |
| occurred_at | TEXT | ISO timestamp |
| raw_payload | TEXT | full webhook JSON (or synthetic equivalent), for audit |
| is_simulated | INTEGER | 0/1 — was this a real Razorpay event or synthetic |

### `cases` — one row per at-risk revenue case being tracked
| Column | Type | Notes |
|---|---|---|
| id | TEXT PK | UUID |
| event_id | TEXT FK → events.id | |
| risk_score | REAL | deterministic score, 0–1 |
| diagnosis | TEXT | LLM-generated root-cause explanation |
| recommended_action | TEXT | retry / payment_link / escalate / stop |
| status | TEXT | pending / recovering / recovered / escalated / stopped |
| created_at | TEXT | ISO timestamp |

### `actions` — every action attempted (the audit trail)
| Column | Type | Notes |
|---|---|---|
| id | TEXT PK | UUID |
| case_id | TEXT FK → cases.id | |
| action_type | TEXT | retry / payment_link / escalate / stop |
| policy_check_result | TEXT | allowed / blocked_max_retries / blocked_amount_threshold / blocked_cooldown |
| executed_at | TEXT | ISO timestamp |
| result | TEXT | success / failed / not_executed (if blocked) |
| is_simulated | INTEGER | 0/1 |

### `outcomes` — measured results
| Column | Type | Notes |
|---|---|---|
| id | TEXT PK | UUID |
| case_id | TEXT FK → cases.id | |
| recovered_amount | INTEGER | paise, 0 if not recovered |
| recovered_at | TEXT | ISO timestamp, nullable |
| baseline_would_have_recovered | INTEGER | 0/1 — did the naive-retry baseline recover this case, for comparison |

### `users` — single merchant login (MVP auth)
| Column | Type | Notes |
|---|---|---|
| id | TEXT PK | |
| username | TEXT | |
| password_hash | TEXT | never store plaintext, even for a demo |

## Relationships
- `events` 1 : 1 `cases` (one case per event, for MVP simplicity)
- `cases` 1 : many `actions` (a case can have multiple attempts —
  e.g. retry, then escalate)
- `cases` 1 : 1 `outcomes` (final measured result per case)