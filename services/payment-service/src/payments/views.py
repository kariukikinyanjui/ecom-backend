from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer
from .clients import StripeClient, OrderServiceClient


class PaymentViewSet(viewsets.ModelViewSet):
    '''
    Handle payment creation and status checks
    Implement idempotent payment processing
    '''
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = 'order_id'

    @action(detail=True, methods=['post'])
    def refund(self, request, order_id=None):
        '''Process refund for completed payment'''
        payment = self.get_object()
        serializer = RefundSerializer(data=request.data)
        if serializer.is_valid():
            # Process refund with Stripe
            refund = serializer.save()
            OrderServiceClient().update_order_status(
                payment.order_id,
                'refunded',
                request.auth
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        '''Idempotent payment creation'''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check for existing payment with idempotency key
        existing = Payment.objects.filter(
            order_id=serializer.validated_data['order_id'],
            idempotency_key=serializer.validated_data['idempotency_key']
        ).first()

        if existing:
            return Response(
                self.get_serializer(existing).data,
                status=status.HTTP_200_OK
            )

            # Process payment with Stripe
            stripe_client = StripeClient()
            payment_intent = stripe_client.create_charge(
                serializer.validated_data['order_id'],
                serializer.validated_data['amount'],
                serializer.validated_data['currency'],
                serializer.validated_data['idempotency_key']
            )

            payment = serializer.save(
                status='completed' if payment_intent.status == 'succeeded' else 'failed',
                gateway_transaction_id=payment_intent.id
            )

            # Updated order status
            OrderServiceClient().update_order_status(
                payment.order_id,
                'completed' if payment.status == 'completed' else 'failed',
                request.auth
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
