import stripe
from django.conf import settings
from .models import Order



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


def handle_successful_payment(order, intent):
    
    order_id = intent.get("metadata", {}).get("order_id")

    if not order_id:
        print("No order_id found in PaymentIntent metadata.")
        return

 
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        raise "Order with ID {order_id} not found."


      
    order.pending_status = "C"  # 
    order.stripe_payment_intent_id = intent["id"]
    order.save()

    
    
    
   

