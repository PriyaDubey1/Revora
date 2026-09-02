# Design — Revora

> Status: Deliberately minimal — function over polish, given the 4-day
> timeline. Don't spend build time here beyond what's listed.

## Design language
Clean, fintech-trustworthy — not playful. Streamlit's default theme is
fine; only override what's listed below.

## Colors (status indicators — the one place color actually matters)
- 🔴 Red — at risk / escalated
- 🟡 Amber — recovering / in progress
- 🟢 Green — recovered
- ⚪ Grey — stopped (policy decided no further action)

## Fonts
Streamlit default (system font stack). Not worth customizing.

## Key screens
1. Summary view — at-risk ₹, recovered ₹, recovery rate vs. baseline,
   cost per recovery (4 top-line numbers)
2. Risk queue table — one row per case, status color-coded
3. Case detail (audit trail) — signals → diagnosis → decision → policy
   check → action → outcome, in that order, for one case