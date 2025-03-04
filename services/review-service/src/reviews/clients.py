import requests
from django.conf import settings
from rest_framework.exceptions import PermissionDenied


class AuthServiceClient:
    '''
    Verifies JWT tokens and user permissions with auth-service
    '''
    def __init__(self):
        self.base_url = settings.AUTH_SERVICE_URL

    def verify_token(self, token):
        '''Validate JWT authenticity'''
        try:
            response = requests.get(
                f"{self.base_url}/api/verify/",
                headers={'Authorization': f'Bearer {token}'}
            )
            return response.status_code == 200
        except requests.ConnectionError:
            raise PermissionDenied("Authentication service unavailable")

    def get_user_id(self, token):
        '''Extract user ID from valid JWT'''
        response = requests.get(
            f"{self.base_url}/api/me/",
            headers={'Authorization': f'Bearer {token}'}
        )
        return response.json().get('id')
