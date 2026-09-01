# Product Requirements Document (PRD) — Revora

> Track 03: AI Revenue Recovery — Razorpay Buildathon. Status: LOCKED for the 4-day build (1–5 Sept). Do not expand scope past this document without updating it first.

## 1. Problem Statement

**What problem does this solve?**
Subscription businesses lose 5–10% of monthly recurring revenue to failed
recurring payments (expired cards, insufficient funds, bank blocks, network
issues). Most companies apply the same blunt 1–2 automatic retries to every
failure regardless of cause or customer history — so genuine, recoverable
revenue is lost simply because no one (and no smart system) followed up
correctly.

**Who experiences this problem?**
Any subscription/recurring-billing merchant (SaaS, OTT, gyms, subscription
boxes) on Razorpay. In this project, represented by a synthetic merchant,
**FitFlow** — 10,000 subscribers, ₹999/month.

**Why does this problem matter now?**
It's a direct, measurable P&L hit (₹5–10L/month lost on ₹1Cr revenue at
typical fail rates), not a hypothetical one — which is why Razorpay made it
a dedicated buildathon track.

## 2. Target User

**Primary (in-product) user: the merchant's ops/finance person.**
- Role: someone responsible for MRR/revenue health at a subscription
  business, not a payments engineer.
- Goals: recover as much at-risk revenue as possible without manual,
  case-by-case chasing; trust that the system won't do anything reckless
  with customer charges.
- Frustrations: current tools are either a black box ("trust our AI") or
  pure static retry logic with no reasoning; no visibility into *why* an
  action was taken, no audit trail for compliance conversations.
- Behavior: logs into a dashboard periodically to check at-risk revenue
  and recovered revenue, not a real-time/always-on user for v1.

**Secondary (evaluation) audience: buildathon judges.**
They will interact with the same dashboard and question "how much did you
recover, on what batch, and can you prove it" — this shapes what the UI
must surface, not a separate feature set.

## 3. Core Features (MVP Only)

1. **Detect + Diagnose** — Ingests failed-payment signals (via Razorpay
   webhook or synthetic batch), extracts signals (failure reason, past
   success rate, days since last success, amount), and produces a
   deterministic risk score + an LLM-generated plain-language root-cause
   explanation.
2. **Decide + Policy** — Selects a recovery strategy (retry / send payment
   link / escalate to human / stop) using an expected-value calculation,
   then checks it against deterministic policy guardrails (max retries,
   high-value human-approval threshold, cooldown/stopping rules) before
   anything is allowed to execute.
3. **Execute** — Carries out the approved action via the Razorpay
   test-mode API (adapter pattern; a subset of cases hit the real
   test-mode API, the rest run through a simulator for batch scale),
   logging every action as an audit record.
4. **Measure** — Runs the full pipeline across a batch of synthetic
   failed-payment cases, computes recovered ₹ and recovery rate vs. a
   naive-retry baseline on the *same* batch, and computes cost-per-recovery
   (AI/API cost ÷ recovered cases).
5. **Merchant Login + Dashboard** — Simple single-merchant login (not
   multi-tenant SaaS auth — see Non-Goals), showing: at-risk revenue queue,
   recovered ₹ and recovery rate (with baseline comparison), cost per
   recovery, and a searchable audit trail per case.

**Nice to Have (not needed for launch):**
- Hinglish/voice-based merchant interaction
- Multi-merchant/multi-tenant support
- Email/SMS actually sent to end-customers (vs. logged as "would send")

## 4. Out of Scope (Explicit Non-Goals)

- **Multi-tenant SaaS auth, billing, or onboarding flows** — one hardcoded
  demo merchant login is enough.
- **Live/production Razorpay payments** — test mode only, real money never
  moves.
- **ML model training / precision-recall claims** — no labeled dataset,
  no train/val/test split. We use a transparent scoring formula, not a
  trained classifier, and we do not claim ML metrics we haven't earned.
- **Checkout drop-off recovery and receivables tracking** — those are
  separate Track 3 sub-problems; Revora is depth-not-breadth on failed
  *subscription* payments only.
- **Postgres/Celery/production job queues** — SQLite + synchronous
  execution is enough at MVP batch scale (300–500 events).
- **Mobile app / browser extension** — web dashboard only.
- **Security pentesting / compliance certification** — out of scope for a
  4-day buildathon MVP.

## 5. Success Metrics

1. **Recovery rate on a synthetic batch** (primary KPI) — % of at-risk
   revenue recovered by Revora vs. a naive-single-retry baseline, on the
   *same* 300–500 event batch. This is the headline number for judges.
2. **Cost per recovery** — total AI/API cost of the batch run ÷ number of
   successfully recovered cases. Chosen specifically because Slicker and
   similar black-box tools don't expose unit economics — this is a
   deliberate differentiator, not just a vanity metric.
3. **Zero policy violations** — count of actions that would have breached
   a guardrail (should always be 0, since guardrails block before
   execution) — proves the deterministic/probabilistic split actually
   holds under load, not just in the demo's happy path.

## 6. Technical Assumptions

- **Stack:** Python + FastAPI (backend) + SQLite (storage) + Streamlit
  (dashboard) + Claude API (reasoning/explanation, structured JSON output)
- **Platform:** Web only
- **Integrations:** Razorpay test-mode API (Subscriptions, Webhooks,
  Payment Links); Anthropic Claude API
- **Auth:** Single hardcoded merchant login (username/password or simple
  session token) — enough to demonstrate the concept, not production auth
- **Why this stack:** speed-to-working-demo over polish, given the 4-day
  deadline (see `TechSpec.md` and `ImplementationPlan.md`)

## 7. Competitive Positioning

**Reference: Slicker** (YC-backed, Stripe/Chargebee/Recurly-focused AI
payment recovery tool) — an ensemble ML model that silently picks retry
timing and dunning messages, prices on a pay-for-success basis, and does
not expose its reasoning or unit economics to the merchant.

**Revora's explicit differentiation:**
- **Explainable, not black-box** — every decision comes with a
  human-readable root-cause explanation, not just an action.
- **Policy-bounded by design** — deterministic guardrails (retry limits,
  approval thresholds, stopping rules) sit between the AI's reasoning and
  any money-moving action; this is architecturally enforced, not a
  dashboard setting.
- **Audit-first** — every action, allowed or blocked, is logged with why —
  built for a compliance conversation, not just a growth-metrics review.
- **Cost transparency** — cost-per-recovery is a first-class metric,
  not hidden inside a performance-based pricing model.
- **Razorpay/India-native**, vs. Slicker's Stripe/US-centric integrations.

## 8. Open Questions

1. Real Razorpay test-mode webhook flow vs. simulator — resolved once the
   Day 0 POC runs (see `Tracker.md`); may force a scope note in the
   submission's "what broke" doc.
2. Exact expected-value formula for the risk/strategy score — needs to be
   nailed down and documented (not left as "a simple model") before Day 1
   ends.
3. What merchant login mechanism is fastest to build correctly in the time
   available (plain session cookie vs. something more) — decide at Day 1.
4. Exact policy threshold values (max retries, high-value ₹ cutoff) still
   need one-line justifications each — placeholder reasoning to be added
   during Day 2 build.
5. Whether the pitch video shows the Slicker comparison explicitly or
   keeps it implicit in the explainability/audit framing — decide during
   Day 4 script writing.