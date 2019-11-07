# Token authentication
import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User

class JWTAuthentication(authentication.BaseAuthentication):

    """ Authenticate token passed in the auth header """

    def authenticate(self, request):
        # AUthenticate auth token
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header:
            return None

        token_key = auth_header[0].decode('utf-8')
        auth_token = auth_header[1].decode('utf-8')
        
        if len(auth_header) < 2 or len(auth_header) > 2:
            msg = 'Invalid authorization header'
            raise exceptions.AuthenticationFailed(msg)

        if token_key != 'Bearer':
            msg = 'Bearer header required'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(request, auth_token)

    
    def authenticate_credentials(self, request, token):
        # First try to decode the token
        # then fetch the user data that concides with the user email
        # check if token has expired and raise a validation error
        # for user to get a new token
        # ONLY when the token is valid return the user and the decoded payload
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(email=payload["email"])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'Token has expired please request for another'
            )
        return (user, payload)