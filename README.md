# Revora — Day 0 Setup

Track 03: AI Revenue Recovery — Razorpay Buildathon Track 3

## What this is (right now)

This is the **Day 0 skeleton**: just enough to verify that the Razorpay
test-mode subscription + webhook flow actually works before we build the
real pipeline on top of it. Don't add more here until the POC passes.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# now edit .env and paste in your real RAZORPAY_KEY_ID / RAZORPAY_KEY_SECRET
```

## Step 1 — Run the subscription POC

```bash
python pipeline/poc_test_subscription.py
```

This creates a plan, customer, and subscription, and prints a URL to
authorize it with a test card. Follow the printed instructions.

## Step 2 — Get webhooks flowing

In one terminal:
```bash
uvicorn pipeline.webhook_server:app --reload --port 8000
```

In another terminal (install ngrok first: https://ngrok.com/download):
```bash
ngrok http 8000
```

Copy the `https://xxxx.ngrok-free.app` URL ngrok gives you. In the
Razorpay Dashboard: **Account & Settings → Webhooks → Add New Webhook**
- Webhook URL: `https://xxxx.ngrok-free.app/webhook/razorpay`
- Active events: `subscription.charged`, `subscription.pending`,
  `subscription.halted`, `payment.failed`
- Copy the **Webhook Secret** shown there into your `.env` as
  `RAZORPAY_WEBHOOK_SECRET`

## Step 3 — Trigger a failure and watch it arrive

In the Dashboard, open your subscription (Subscriptions tab) and use
**"Charge this now"** to manually simulate a failed charge. Watch your
`uvicorn` terminal — you should see the event logged.

**If this works: we're unblocked, move to Day 1 (synthetic data +
Detect/Diagnose stage).**

**If webhooks won't arrive / ngrok is a pain right now:** don't burn more
than ~2 hours on it. Fall back to a simulator that fabricates the same
webhook JSON shape locally — flag this decision in the "what broke and
how you recovered" doc for submission. That failure-and-recovery story is
literally something the judges want to see.

## Project structure (target — build this incrementally)

```
razorrecover/
├── pipeline/
│   ├── razorpay_client.py      # adapter (done)
│   ├── webhook_server.py       # webhook intake (done)
│   ├── poc_test_subscription.py
│   ├── detect.py               # Day 1
│   ├── decide_policy.py        # Day 2
│   ├── execute.py              # Day 2
│   └── outcome.py              # Day 3
├── data/                       # synthetic dataset + generator
├── dashboard/                  # Streamlit app
├── tests/                      # policy rule tests
├── .env.example
└── README.md
```
