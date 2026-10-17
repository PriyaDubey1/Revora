# pipeline/api_server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pipeline.agents import analyze_root_cause_and_recommend
from pipeline.policy_engine import PolicyEngine
from pipeline.audit_logger import AuditLogger
from simulator.batch_eval import generate_synthetic_data

app = FastAPI(title="Revora API", version="1.0")

# Enable CORS for Next.js Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "online", "system": "Revora AI Revenue Recovery Agent"}

@app.get("/api/v1/dashboard/metrics")
def get_dashboard_metrics():
    # Live stats for Dashboard Screen 1
    return {
        "revenue_at_risk": 772340000,   # in paise (₹77.23L)
        "recoverable": 515613600,       # in paise
        "recovered": 58922700,          # in paise (₹5.89L)
        "recovery_rate": 7.63,          # percentage
        "actions_executed": 398,
        "policy_blocks": 602
    }

@app.get("/api/v1/risk-queue")
def get_risk_queue():
    # Sample Risk Queue for Screen 2
    raw_data = generate_synthetic_data(10)
    queue = []
    for item in raw_data:
        ai_out = analyze_root_cause_and_recommend(item)
        policy_out = PolicyEngine.evaluate(
            action_proposal={"action": ai_out["recommended_action"]},
            subscription_context={"retry_count": item["retry_count"], "amount": item["amount"]}
        )
        queue.append({
            "event": item,
            "ai_investigation": ai_out,
            "policy": policy_out
        })
    return queue

@app.post("/api/v1/investigate")
def investigate_event(failed_event: dict):
    # Single Case Investigation Endpoint for Screen 3
    ai_out = analyze_root_cause_and_recommend(failed_event)
    policy_out = PolicyEngine.evaluate(
        action_proposal={"action": ai_out["recommended_action"]},
        subscription_context={"retry_count": failed_event.get("retry_count", 0), "amount": failed_event.get("amount", 0)}
    )
    
    audit_entry = None
    if policy_out["policy_decision"] == "approved":
        audit_entry = AuditLogger.log_decision(
            failed_event=failed_event,
            ai_output=ai_out,
            policy_output=policy_out,
            result="success",
            amount_recovered=failed_event.get("amount", 0)
        )

    return {
        "ai_output": ai_out,
        "policy_output": policy_out,
        "audit_entry": audit_entry
    }