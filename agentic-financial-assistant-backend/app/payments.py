import stripe
from app.config import settings
from fastapi import HTTPException

stripe.api_key = settings.stripe_secret_key

async def create_stripe_payment_intent(amount: float, currency: str = "usd", metadata: dict = None):
    # Stripe expects amount in cents
    amount_cents = int(round(amount * 100))
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=currency,
            metadata=metadata or {}
        )
        return intent
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def verify_stripe_event(payload: bytes, sig_header: str):
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
        return event
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail=f"Webhook signature verification failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
