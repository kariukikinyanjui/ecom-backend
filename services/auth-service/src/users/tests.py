from django.urls import reverse
from rest_framework.test import APITestCase
from .models import User


class AuthTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )

    # Test Registration
    def test_user_registration(self):
        url = reverse('register')
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue("access" in response.data)

    # Test Login
    def test_valid_login(self):
        url = reverse('login')
        data = {"username": "testuser", "password": "wrongpass"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)

    # Test Token Refresh
    def test_token_refresh(self):
        # First login to get tokens
        login_url = reverse('login')
        login_data = {"username": "testuser", "password": "testpass123"}
        login_response = self.client.post(login_url, login_data)
        refresh_token = login_response.data["refresh"]

        # Refresh token
        refresh_url = reverse('token_refresh')
        response = self.client.post(refresh_url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("access" in response.data)
