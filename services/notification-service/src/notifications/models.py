from django.db import models


class Notification(models.Model):
    '''
    Tracks all notification attempts and their statuses
    Store references to external service IDs (users/orders)
    '''
    class Types(models.TextChoices):
        EMAIL = 'email', 'Email'
        SMS = 'sms', 'SMS'
        PUSH = 'push', 'Push Notification'

    user_id = models.UUIDField() # from auth-service
    notification_type = models.CharField(max_length=20, choices=Types.choices)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('sent', 'Sent'),
            ('failed', 'Failed')
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_id', '-created_at']),
        ]
        ordering = ['-created_at']
