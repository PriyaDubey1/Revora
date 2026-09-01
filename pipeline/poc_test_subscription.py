"""
DAY 0 POC — run this FIRST, before writing any more pipeline code.

Goal: prove that in Razorpay TEST MODE we can:
  1. Create a plan
  2. Create a customer
  3. Create a subscription
  4. Get a short_url to authorize the subscription with a TEST card
  5. See the subscription's state change (webhook / fetch)

This de-risks the whole project. If this doesn't work smoothly, we switch
to a simulator-only plan immediately instead of losing a day to it later.

HOW TO RUN:
  1. cd razorrecover
  2. python -m venv venv && source venv/bin/activate   (Windows: venv\\Scripts\\activate)
  3. pip install -r requirements.txt
  4. cp .env.example .env   and fill in your real RAZORPAY_KEY_ID / SECRET
  5. python pipeline/poc_test_subscription.py
"""
from pipeline.razorpay_client import (
    create_plan,
    create_customer,
    create_subscription,
    fetch_subscription,
)

def main():
    print("Step 1: Creating a test plan (₹999/month)...")
    plan = create_plan(amount_paise=99900, item_name="RazorRecover FitFlow Plan")
    print(f"  Plan created: {plan['id']}")

    print("\nStep 2: Creating a test customer...")
    customer = create_customer(
        name="Test Customer",
        email="test.customer@example.com",
        contact="9999999999",
    )
    print(f"  Customer created: {customer['id']}")

    print("\nStep 3: Creating a subscription...")
    subscription = create_subscription(plan_id=plan["id"])
    print(f"  Subscription created: {subscription['id']}")
    print(f"  Status: {subscription['status']}")
    print(f"  Authorize this subscription (open in browser): {subscription['short_url']}")

    print("\n--- NEXT STEPS ---")
    print("1. Open the short_url above in a browser to authorize the")
    print("   subscription (any test card works, e.g. 4111 1111 1111 1111,")
    print("   any future expiry, any CVV, OTP 4+ digits = success).")
    print("   Full test card list: https://razorpay.com/docs/payments/payments/test-card-details/")
    print("2. Go to Dashboard > Subscriptions > open this subscription.")
    print("   Razorpay test mode has a 'Charge this now' button that lets")
    print("   you MANUALLY trigger a charge attempt and choose success or")
    print("   failure — this is the reliable way to simulate a failed")
    print("   renewal (moves subscription to 'pending', fires the real")
    print("   subscription.pending webhook) without waiting for the actual")
    print("   billing date. Details: https://razorpay.com/docs/payments/subscriptions/test/")
    print("3. Re-fetch the subscription below to see its state change:\n")

    refreshed = fetch_subscription(subscription["id"])
    print(f"  Current status: {refreshed['status']}")

    print("\nIf you got this far without errors, the integration works.")
    print("Save this subscription_id, customer_id, and plan_id — you'll want")
    print("them for building the synthetic data generator on the same shape.")


if __name__ == "__main__":
    main()
