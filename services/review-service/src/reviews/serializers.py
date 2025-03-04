from rest_framework import serializers
from .models import Review, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user_id', 'text', 'created_at']
        read_only_fields = ['user_id', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'user_id', 'product_id', 'rating',
            'title', 'body', 'is_approved', 'comments',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user_id', 'is_approved']

    def validate_rating(self, value):
        if not 1 <= value <=5:
            raise serializers.ValidationError("Rating must be between 1-5")
        return value
