# authentication.py
from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    """
    Custom authentication class that uses 'Bearer' keyword instead of 'Token'
    """

    keyword = "Bearer"
