"""
Webhook receiver for Razorpay events.

Run: uvicorn pipeline.webhook_server:app --reload --port 8000

To expose this to Razorpay's servers for testing, use ngrok:
  ngrok http 8000
Then register the ngrok https URL as your webhook URL in:
  Dashboard > Account & Settings > Webhooks
Subscribe to at least: subscription.charged, subscription.pending,
subscription.halted, payment.failed
"""
import os
import json
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
from pipeline.razorpay_client import verify_webhook_signature

load_dotenv()

app = FastAPI(title="RazorRecover Webhook Receiver")

WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET")

# Naive in-memory idempotency store for the POC. Replace with a DB table
# (event_id UNIQUE) before the real pipeline runs on a batch.
_seen_event_ids = set()


@app.post("/webhook/razorpay")
async def razorpay_webhook(request: Request):
    raw_body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature")

    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature header")

    if not WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")

    is_valid = verify_webhook_signature(
        payload=raw_body.decode("utf-8"),
        signature=signature,
        webhook_secret=WEBHOOK_SECRET,
    )
    if not is_valid:
        # Never trust an unsigned/invalid event — this is the #1 fintech
        # webhook mistake (fake events triggering real actions).
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    payload = json.loads(raw_body)
    event_id = request.headers.get("X-Razorpay-Event-Id") or payload.get("id")
    event_type = payload.get("event")

    if event_id in _seen_event_ids:
        # Idempotency: duplicate delivery of an event we already processed.
        return {"status": "duplicate_ignored"}
    _seen_event_ids.add(event_id)

    print(f"[webhook] event={event_type} id={event_id}")

    # TODO (Day 1): route this into the Detect/Diagnose stage instead of
    # just printing it. Keep this file dumb — persistence + routing lives
    # in a separate module so this stays easy to reason about.

    return {"status": "received", "event": event_type}


@app.get("/health")
def health():
    return {"status": "ok"}
