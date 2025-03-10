from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'user_id', 'notification_type',
            'subject', 'message', 'status', 'created_at'
        ]
        read_only_fields = ['status', 'created_at']

    def validate_notification_type(self, value):
        if value not in Notification.Types.values:
            raise serializers.ValidationError("Invalid notification type")
        return value
