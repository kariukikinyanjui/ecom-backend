from rest_framework.permissions import BasePermission
from .utils import AuthServiceClient

class IsAdminUser(BasePermission):
    """Verify admin status via auth-service"""
    def has_permission(self, request, view):
        client = AuthServiceClient()
        if not client.verify_token(request.auth):
            return False
        return client.is_admin(request.auth)
