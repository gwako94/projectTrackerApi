import os
import datetime
import jwt

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.conf import settings

class UserManager(BaseUserManager):
    """ 

    Custom manager class to override `create_user` method to create 
    `User` objects

    """

    def create_user(self, username, email, password=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ User Model """
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.email


    @property
    def token(self):
        """Generate a user token"""
        try:
            token = jwt.encode({
                "id": self.pk,
                'username': self.username,
                'email': self.email,
                'iat': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=int(
                    os.getenv("EXPIRES_AFTER", 15)
                ))

            }, settings.SECRET_KEY, algorithm="HS256").decode()
        except jwt.PyJWTError:
            token = ""
        return token
