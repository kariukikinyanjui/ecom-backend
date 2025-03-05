from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''
    Custom User model extending Django's build-in AbstractUser.
    This model is designed to provide additional flexibility for user management
    within the authentication service. It overries or adds fields as needed
    while maintaining compatibility with Django's authentication system.
    '''
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        # Isolated table name for the auth service
        db_table = "auth_users"

    def __str__(self):
        '''
        String representation of the User object.

        Returns:
            str: The username of the user.
        '''
        return self.username
