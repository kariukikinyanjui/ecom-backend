import requests
from django.conf import settings


class AuthServiceClient:
    '''
    Client for communicating with auth-service
    Handles JWT validation and permission checks
    '''

    def __init__(self):
        self.base_url = settings.AUTH_SERVICE_URL

    def verify_token(self, token):
        '''Validate JWT with auth-service'''
        response = requests.get(
            f"{self.base_url}/api/verify/",
            headers={'Authorization': f'Bearer {token}'}
        )
        return response.status_code == 200

    def is_admin(self, token):
        '''Check if user has admin privileges'''
        response = requests.get(
            f"{self.base_url}/api/me/",
            headers={'Authoerization': f'Bearer {token}'}
        )
        return response.json().get('is_staff', False)
