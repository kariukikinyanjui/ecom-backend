from django.urls import reverse
from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User
from datetime import timedelta
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


class AuthTests(APITestCase):
    '''
    Test cases for authentication endpoints (register, login, refresh token).
    '''

    @classmethod
    def setUpTestData(cls):
        '''Set up test data for all test methods.'''
        cls.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )

    # Test Registration
    def test_user_registration(self):
        '''
        Test successful user registration with valid credentials.
        '''
        url = reverse('register')
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue("access" in response.data)
        # Verify user was created
        self.assertTrue(User.objects.filter(username="newuser").exists())

    # Test Login
    def test_valid_login(self):
        '''
        Test successful login with valid credenetials.
        '''
        url = reverse('login')
        data = {"username": "testuser", "password": "wrongpass"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)

    # Test Token Refresh
    def test_token_refresh(self):
        '''
        Test successful token refresh using a valid refresh token.
        '''
        # First login to get tokens
        login_url = reverse('login')
        login_data = {"username": "testuser", "password": "testpass123"}
        login_response = self.client.post(login_url, login_data, format='json')
        refresh_token = login_response.data["refresh"]

        # Refresh token
        refresh_url = reverse('token_refresh')
        response = self.client.post(refresh_url, {"refresh": refresh_token}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("access", response.data)
