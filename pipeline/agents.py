# pipeline/agents.py
import json

def analyze_root_cause_and_recommend(failure_event: dict) -> dict:
    """
    Simulates AI analysis for root cause & action selection.
    Integrate OpenAI/Claude API here for live LLM call.
    """
    amount = failure_event.get("amount", 0)
    retry_count = failure_event.get("retry_count", 0)
    
    # Contextual strategy decision
    if retry_count < 2 and amount <= 1000000:
        recommended_action = "retry"
        reason = "Transient failure detected; automated retry suggested."
    else:
        recommended_action = "payment_link"
        reason = "Direct retry threshold exceeded; recovery via payment link recommended."

    return {
        "root_cause": "Payment gateway timeout / card authorization failure",
        "evidence": [f"Retry count: {retry_count}", f"Amount: ₹{amount/100}"],
        "recommended_action": recommended_action,
        "expected_recovery": 0.75,
        "reasoning": reason
    }