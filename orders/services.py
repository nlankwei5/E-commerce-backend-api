import stripe
from django.conf import settings



def stripe_payment_intent(order):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    total_amount = int(order.grand_total * 100)
    payment_intent = stripe.PaymentIntent.create(
        amount=total_amount,
        currency="usd",
        automatic_payment_methods={"enabled": True},
        metadata={'order_id': order.id}
    )
    order.stripe_payment_intent_id = payment_intent.id
    order.save()
    return payment_intent.client_secret

