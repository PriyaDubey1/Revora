"""
Thin adapter around the Razorpay SDK.

Why an adapter? So the rest of the pipeline never talks to `razorpay` directly.
If Razorpay is unreachable/rate-limited during the demo, we swap this file's
implementation for a simulator without touching any other code (see
`simulator_client.py`, added later).
"""
import os
import razorpay
from dotenv import load_dotenv

load_dotenv()

KEY_ID = os.getenv("RAZORPAY_KEY_ID")
KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

if not KEY_ID or not KEY_SECRET:
    raise RuntimeError(
        "RAZORPAY_KEY_ID / RAZORPAY_KEY_SECRET not set. "
        "Copy .env.example to .env and fill in your test-mode keys."
    )

client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


def create_plan(amount_paise: int, interval: int = 1, period: str = "monthly",
                 item_name: str = "RazorRecover Test Plan"):
    """Create a subscription plan. amount is in paise (e.g. 99900 = ₹999)."""
    return client.plan.create({
        "period": period,
        "interval": interval,
        "item": {
            "name": item_name,
            "amount": amount_paise,
            "currency": "INR",
        },
    })


def create_customer(name: str, email: str, contact: str):
    return client.customer.create({
        "name": name,
        "email": email,
        "contact": contact,
    })


def create_subscription(plan_id: str, customer_notify: int = 1, total_count: int = 12):
    """Create a subscription against a plan. Returns the subscription object
    which includes a `short_url` you can open to complete the (test-mode)
    authorization payment."""
    return client.subscription.create({
        "plan_id": plan_id,
        "customer_notify": customer_notify,
        "total_count": total_count,
    })


def fetch_subscription(subscription_id: str):
    return client.subscription.fetch(subscription_id)


def verify_webhook_signature(payload: str, signature: str, webhook_secret: str) -> bool:
    """Validate that a webhook actually came from Razorpay before trusting it."""
    try:
        client.utility.verify_webhook_signature(payload, signature, webhook_secret)
        return True
    except razorpay.errors.SignatureVerificationError:
        return False
