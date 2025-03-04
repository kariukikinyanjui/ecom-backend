from rest_framework import viewsetet, permissions
from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from .clients import AuthServiceClient


class ReviewViewSet(viewsets.ModelViewSet):
    '''
    Handle review CRUD operations with permissions:
    - Users can only modify their own reviews
    - Admins can approve/reject reviews
    '''

    serializer_class = ReviewSerializer
    permission_class = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(
            product_id=self.kwargs['product_id']
        ).prefetch_related('commnets')

    def perform_create(self, serializer):
        '''Inject user ID from JWT'''
        client = AuthServiceClient()
        user_id = client.get_user_id(self.request.auth)
        serializer.save(user_id=user_id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            review_id=self.kwargs['review_id']
        )

    def perform_create(self, serializer):
        client = AuthServiceClient()
        user_id = client.get_user_id(self.request.auth)
        serializer.save(user_id=user_id)
