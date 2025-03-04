import stripe
from django.conf import settings
from rest_framework.exceptions import APIException


class StripeClient:
    '''
    Stripe payment processor integration
    Handles charges, refunds, and webhook verification
    '''

    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    def create_charge(self, order_id, amount, currency, idempotency_key):
        '''Create a payment intent with idempotency'''
        try:
            return stripe.PaymentIntent.create(
                amount=int(amount * 100), # Convert to cents
                currency=currency.lower(),
                metadata={'order_id': str(order_id)},
                idempotency_key=str(idempotency_key)
            )
        except stripe.error.StripeError as e:
            raise APIException(f"Stripe error: {e.user_message}")

    def verify_webhook(self, payload, signature):
        '''Validate webhook authenticity'''
        try:
            return stripe.Webhook.construct_even(
                payload, signature, self.webhook_secret)
        except ValueError as e:
            raise APIException("Invalid payload")
        except stripe.error.SignatureVerificationError as e:
            raise APIException("Invalid signature")


class OrderServiceClient:
    '''Client to update order status in order-service'''
    def __init__(self):
        self.base_url = settings.ORDER_SERVICE_URL

    def update_order_status(self, order_id, status, auth_token):
        try:
            response = requests.patch(
                f"{self.base_url}/orders/{order_id}/",
                json={'status': status},
                headers={'Authentication': f'Bearer {auth_token}'}
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise APIException(f"Order service error: {str(e)}")
