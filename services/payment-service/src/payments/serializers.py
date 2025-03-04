from rest_framework import serializers
from .models import Payment, Refund


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'order_id', 'amount', 'currency', 'status',
            'payment_gateway', 'created_at'
        ]
        read_only_fields = ['status', 'created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidateError("Amount must be positive")
        return value


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = ['id', 'payment', 'amount', 'reason', 'created_at']
        read_only_fields = ['created_at']
