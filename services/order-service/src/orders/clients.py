import requests
from django.conf import settings
from rest_framework.exceptions import APIException


class ProductServiceClient:
    '''
    Client for communicating with product-service
    Handles product validation and price verification
    '''
    def __init__(self):
        self.base_url = settings.PRODUCT_SERVICE_URL

    def get_product(self, product_id: str, token: str) -> dict:
        '''Verify product existence and get current price'''
        try:
            response = request.get(
                f"{self.base_url}/products/{product_id}/",
                headers={'Authorization': f'Bearer {token}'}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIException(f"Product service error: {str(e)}")
