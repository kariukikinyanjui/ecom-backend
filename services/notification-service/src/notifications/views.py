from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from .clients import EmailClient
from .tasks import send_email_async


class NotificationViewSet(viewsets.ModelViewSet):
    '''
    Handle notification requests with async processing
    - Email notifications are sent via Celery workers
    - Immediate response with notification status
    '''
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        notification = serializer.save()

        # Queue email sending for async processing
        if notification.notification_type == 'email':
            send_email_async.delay(
                notification.id,
                notification.subject,
                notification.message
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
