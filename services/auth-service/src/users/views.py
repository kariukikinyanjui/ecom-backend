from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import serializers
from .models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class LoginResponseSerializer(serializers.Serializer):
    user = UserSerializer() # Correct nested serializer declaration
    refresh = serializers.CharField()
    access = serializers.CharField()


class RegisterView(APIView):
    '''
    API View for user registration.

    Handles POST requests to create a new user and return JWT tokens upon successful registration.

    Endpoint: /register/
    '''
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
            400: "Bad Request"
            },
        operation_description="Register a new user and get JWT tokens."
    )

    def post(self, request):
        '''
        Handle user registration.

        Args:
            request (Request): The incoming HTTP request containing user data.
        Returns:
            Response:
            - 201 Created: Returns user data, refresh token, and access token on sucess.
            - 400 Bad request: Returns validation erros if data is invalid.
        '''

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() # save the user to the database
            refresh = RefreshToken.for_user(user) # generate JWT tokens
            return Response({
                "user": serializer.data, # serialized user data
                "refresh": str(refresh), # refresh token for obtaining new access tokens
                "access": str(refresh.access_token), # short-lived access token for API requests
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    '''
    Handle user login and token generation.

    Args:
        request (Request): The incoming HTTP request containing user credentials.

    Returns:
        Response:
            - 200 OK: Returns user data, refresh token, and access token on successful authentication.
            - 401 Unauthorized: Returns an error if authentication fails.
    '''
    @swagger_auto_schema(
            operation_description="Authenticate user and get tokens",
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=['username', 'password'],
                properties={
                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                    'password': openapi.Schema(type=openapi.TYPE_STRING),
                }
            ),
            responses={
                200: LoginResponseSerializer,
                401: "Invalid credentials"
            }
     ) 

    def post(self, request):
        '''
        Handle user login and token generation.

        Args:
            request (Request): The incoming HTTP request containing user credentials.
        Return:
            Response:
                - 200 OK: Returns user data, refresh token, and access token on successful authentication.
                - 401 Unauthorized: Returns an error if authentication fails.
        '''
        username = request.data.get('username')
        password = request.data.get('password')

        # Validate credentials using Django's authentication backend
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate JWT tokens (refresh and access)
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data, # serialized user details
            "refresh": str(refresh),           # refresh token for obtaining new access tokens
            "access": str(refresh.access_token), # short-lived access token for API request
        }, status=status.HTTP_200_OK)


class RefreshTokenView(TokenRefreshView):
    '''
    API View for refreshing JWT access tokens.

    Extends the default `TokenRefreshView` to customize the response format.

    Endpoint: /refresh/
    '''
    @swagger_auto_schema(
        operation_description='Refresh access token',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response(
                description='Token refreshed successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            401: 'Invalid or expired refresh token'
        }
    )

    def post(self, request, *args, **kwargs):
        '''
        Override the POST method to customize the response.

        Args:
            request (Request): The incoming HTTP request containing the refresh token.
        Returns:
            Response:
                - 200 OK: Returns the new access token.
                - 400 Unauthorized: Returns an error in the refresh token is invalid/expired
        '''

        # call the superclass to handle token refresh logic
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # customize the response to return only the "access" token
            return Response({
                "access": response.data["access"]
            }, status=status.HTTP_200_OK)
        return response # Propagate any errors


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "email": request.user.email
        })
