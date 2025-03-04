from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    '''
    Stores product reviews with ratings and user associations
    user_id and product_id reference external service UUIDs
    '''

    user_id = models.UUIDField() # from auth-service
    product_id = models.UUIDField() # from product-service
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=100)
    body = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['product_id', '-created_at']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'product_id'],
                name='one_review_per_product'
            )
        ]


class Comment(models.Model):
    '''Nested comments on reviews'''
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    user_id = models.UUIDField() # from auth-service
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
