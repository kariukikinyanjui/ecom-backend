from django.db import models
from django.core.validators import MinValueValidator
import uuid


class Payment(models.Model):
    '''
    Represents a payment attempt with audit trail
    Linked to orders via UUID from order-service
    '''

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'

    order_id = models.UUIDField() # From order-service
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    payment_gateway = models.CharField(max_length=20) # stripe/paypal
    gateway_transaction_id = models.CharField(max_length=100, blank=True)
    idempotency_key = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('order_id', 'idempotency_key')]
        indexes = [
            models.Index(fields=['order_id', '-created_at']),
        ]


class Refund(models.Model):
    '''Track refunds for completed payments'''
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
