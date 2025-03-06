from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    '''
    Serializer for the User model.

    This serializer converts User model instances into JSOn representations and vice versa.
    It specifies which fields are included in the API responses and validates incoming data.
    '''
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'is_staff',
            'last_login'
        )
