from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .clients import StripeClient

@csrf_exempt
def stripe_webhook(request):
    """
    Handle Stripe webhook events:
    - payment_intent.succeeded
    - payment_intent.payment_failed
    - charge.refunded
    """
    payload = request.body
    signature = request.headers.get('Stripe-Signature')
    stripe_client = StripeClient()

    try:
        event = stripe_client.verify_webhook(payload, signature)
    except APIException as e:
        return HttpResponse(str(e), status=400)

    # Handle event types
    if event.type == 'payment_intent.succeeded':
        handle_success(event.data.object)
    elif event.type == 'payment_intent.payment_failed':
        handle_failure(event.data.object)
    elif event.type == 'charge.refunded':
        handle_refund(event.data.object)

    return HttpResponse(status=200)

def handle_success(payment_intent):
    """Update payment status from webhook"""
    Payment.objects.filter(
        gateway_transaction_id=payment_intent.id
    ).update(status='completed')

def handle_refund(charge):
    """Record refund in database"""
    payment = Payment.objects.get(gateway_transaction_id=charge.payment_intent)
    Refund.objects.create(
        payment=payment,
        amount=charge.amount_refunded / 100,  # Convert from cents
        reason=charge.reason or "Customer request"
    )
