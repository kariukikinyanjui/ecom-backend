from django.db import models
from django.core.validators import MinValueValidator


class Order(models.Model):
    '''
    Represents a customer order with financial and status tracking
    Stores user reference as UUID from auth-service
    '''
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    user_id = models.UUIDField()  # From auth-service JWT
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_id', '-created_at']),
        ]
        ordering = ['-created_at']


class OrderItem(models.Model):
    '''
    Individual products within an order with historical pricing
    References products via UUID from product-service
    '''

    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product_id = models.UUIDField() # From product-service
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    class Meta:
        unique_together = [('order', 'product_id')]
