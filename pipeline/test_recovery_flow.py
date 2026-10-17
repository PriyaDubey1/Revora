# pipeline/test_recovery_flow.py
from pipeline.agents import analyze_root_cause_and_recommend
from pipeline.policy_engine import PolicyEngine
from pipeline.audit_logger import AuditLogger

def run_test():
    failed_event = {
        "customer_id": "cust_2841",
        "subscription_id": "sub_8291",
        "amount": 199900,  # ₹1,999 in paise
        "retry_count": 1
    }
    
    print("--- 1. INGESTING EVENT ---")
    print(failed_event)

    # 1. AI Analysis
    ai_output = analyze_root_cause_and_recommend(failed_event)
    
    # 2. Policy Check
    policy_output = PolicyEngine.evaluate(
        action_proposal={"action": ai_output["recommended_action"]},
        subscription_context={"retry_count": failed_event["retry_count"], "amount": failed_event["amount"]}
    )

    # 3. Execution & Audit Recording
    if policy_output["policy_decision"] == "approved":
        print(f"\n--- 4. EXECUTING ACTION: {ai_output['recommended_action'].upper()} ---")
        # Simulating successful Razorpay action
        execution_result = "success"
        recovered_amount = failed_event["amount"]
    else:
        execution_result = "blocked"
        recovered_amount = 0

    # 4. Audit Log
    AuditLogger.log_decision(
        failed_event=failed_event,
        ai_output=ai_output,
        policy_output=policy_output,
        result=execution_result,
        amount_recovered=recovered_amount
    )

if __name__ == "__main__":
    run_test()