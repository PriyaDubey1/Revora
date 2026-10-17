# pipeline/audit_logger.py
import json
import uuid
from datetime import datetime

class AuditLogger:
    @staticmethod
    def log_decision(failed_event: dict, ai_output: dict, policy_output: dict, result: str, amount_recovered: int = 0):
        audit_entry = {
            "audit_id": f"RR-{str(uuid.uuid4())[:8].upper()}",
            "customer_id": failed_event.get("customer_id"),
            "subscription_id": failed_event.get("subscription_id"),
            "amount_at_risk": failed_event.get("amount"),
            "detected_reason": ai_output.get("root_cause"),
            "recommended_action": ai_output.get("recommended_action"),
            "policy_decision": policy_output.get("policy_decision"),
            "policy_checks": policy_output.get("policy_checks"),
            "result": result,
            "amount_recovered": amount_recovered,
            "timestamp": datetime.now().isoformat()
        }
        
        print("\n--- 📝 AUDIT TRAIL LOGGED ---")
        print(json.dumps(audit_entry, indent=2))
        return audit_entry