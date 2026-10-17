# pipeline/policy_engine.py

class PolicyEngine:
    MAX_RETRIES = 2
    MAX_AUTO_ACTION_AMOUNT = 1000000  # ₹10,000 in paise
    REQUIRE_HUMAN_APPROVAL_ABOVE = 2500000  # ₹25,000 in paise

    @classmethod
    def evaluate(cls, action_proposal: dict, subscription_context: dict) -> dict:
        retry_count = subscription_context.get("retry_count", 0)
        amount = subscription_context.get("amount", 0)

        checks = {
            "retry_limit": retry_count < cls.MAX_RETRIES,
            "amount_limit": amount <= cls.MAX_AUTO_ACTION_AMOUNT,
            "human_approval": "required" if amount > cls.REQUIRE_HUMAN_APPROVAL_ABOVE else "passed"
        }

        is_approved = checks["retry_limit"] and checks["amount_limit"] and checks["human_approval"] == "passed"

        return {
            "policy_decision": "approved" if is_approved else "blocked",
            "policy_checks": checks
        }