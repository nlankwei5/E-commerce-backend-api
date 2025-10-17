import stripe
from django.conf import settings
from .models import Order
from django.db import transaction
from .tasks import order_created, payment_completed

def handle_order_created(order):
    """
    Called right after an order is successfully created.
    """
    transaction.on_commit(lambda: order_created.delay(order.id))

def handle_payment_confirmed(order_id):
    """
    Called right after an order's payment is confirmed.
    """
    payment_completed.delay(order_id)



def stripe_payment_intent(order):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    total_amount = int(order.grand_total * 100)
    payment_intent = stripe.PaymentIntent.create(
        amount=total_amount,
        currency="usd",
        payment_method="pm_card_visa",
        payment_method_types=["card"],
        confirm=True,
        metadata={'order_id': str(order.id)}
    )
    order.stripe_payment_intent_id = payment_intent.id
    order.save()
    return payment_intent.client_secret


def handle_successful_payment(intent):
    
    order_id = intent.metadata.get("order_id")

    if not order_id:
        print("No order_id found in PaymentIntent metadata.")
        return

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        print(f"Order with ID {order_id} not found.")  
        return  

    # Update order status
    order.pending_status = "C"  
    order.stripe_payment_intent_id = intent.id
    order.save()
    
    handle_payment_confirmed(order_id)
    
    print(f"Order {order_id} marked as completed.")