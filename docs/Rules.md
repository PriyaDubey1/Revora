# Rules (for the AI assistant working on this project)

1. **Never fabricate numbers.** Metrics (recovery %, precision/recall, baseline) are only ever reported after actually running the pipeline on real synthetic data. If asked for a number before it's computed, say so — don't estimate and present as fact.

2. **Verify before implementing.** Before writing code against any Razorpay endpoint, check current official docs (via search) rather than relying on memory — API shapes change.

3. **Keep the LLM/deterministic split strict.** The LLM reasons and explains (root cause, recommended action rationale). It never has final authority over money-moving actions — policy guardrails (retry limits, amount thresholds, human-approval triggers) are plain deterministic code, always checked before execution.

4. **Every action gets an audit record.** No exceptions — if an action is taken (or blocked by policy), it's logged with what, why, and the policy check result.

5. **Idempotency on all webhook/execution paths.** Duplicate events must not cause duplicate actions.

6. **Scope discipline.** Don't add features beyond what ImplementationPlan.md defines for the current day. If something seems valuable but out of scope, note it in PRD.md's non-goals or as a "future work" line — don't build it now.

7. **Fail visibly, not silently.** If something breaks during build (API limitation, webhook delay, LLM error), log it — it becomes material for the "what broke and how you recovered" submission doc, which is a strength, not a weakness, if handled well.

8. **Update Tracker.md** after each meaningful chunk of work, not after every tiny step.
