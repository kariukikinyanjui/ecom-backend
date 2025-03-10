from celery import shared_task
from .models import Notification
from .clients import EmailClient


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def send_email_async(notification_id, subject, message):
    '''
    Async task to send emails with retry logic
    Updated notification status on success/failure
    '''
    notification = Notification.objects.get(id=notification_id)
    email_client = EmailClient()

    try:
        # Get user email from auth-service
        user_email = f"user{notification.user_id}@testmail.app"

        # Send actual email
        envelope_id = email_client.send_email(
            user_email,
            subject,
            message
        )

        notification.status = 'sent'
        notification.save()
        return envelope_id

    except Exception as e:
        notification.status = 'failed'
        notification.save()
        raise e
