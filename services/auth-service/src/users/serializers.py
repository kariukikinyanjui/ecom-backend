from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    '''
    Serializer for the User model.

    This serializer converts User model instances into JSON representations and vice versa.
    It specifies which fields are included in the API responses and validates incoming data.
    '''

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
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        '''
        Create a new user instance with hashed password.

        Args:
            validated_data (dict): Validated data from the serializer.
        Returns:
            User: The newly created user instance
        '''
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
