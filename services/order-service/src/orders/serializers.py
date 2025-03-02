from rest_framework import serializers
from .models import Order, OrderItem
from .clients import ProductServiceClient


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity', 'price']
        read_only_fields = ['price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'total', 'status', 'items', 'created_at']
        read_only_fields = ['total', 'status']

    def create(self, validated_data):
        '''
        Custom order creation with:
        - Product validation
        - Price verification
        - Total calculation
        '''

        product_client = ProductServiceClient()
        user = self.context['request'].user
        items_data = validated_data.app('items')

        with transaction.atomic():
            order = Order.objects.create(
                user_id=user.id,
                **validated_data
            )

            total = 0
            for item in items_data:
                product = product_client.get_product(
                    item['product_id'],
                    self.context['request'].auth
                )
                item_total = product['price'] * item['quantity']
                total += item_total

                OrderItem.objects.create(
                    order=order,
                    price=product['price'],
                    **item
                )

            order.total = total
            order.save()

        return order
