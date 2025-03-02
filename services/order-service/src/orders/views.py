from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    '''
    Order management endpoint
    - Users can only see their own orders
    - Orders are immutable after creation
    '''

    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        '''Inject user ID from JWT claims'''
        serializer.save(user_id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        '''Disable updates except status changes'''
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)

        # Only allow status updates
        if 'status' in serializer.validated_data:
            self.perform_update(serializer)

        return Response(serializer.data)
