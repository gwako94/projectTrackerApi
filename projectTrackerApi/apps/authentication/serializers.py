import re
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex='^[A-Za-z\-\_]+\d*$',
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='The username already exists. Kindly try another.'
        )],
        error_messages={
            'invalid': 'Username cannot only have alphanumeric characters.'
        }
    )
    email = serializers.EmailField(required=True, validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=(
                    'Email already associated with account '
                    'Have you tried logging in.'
                )
            )
        ]
    )

    password = serializers.CharField(min_length=8, required=True,
        error_messages={
            'min_length': 'Password should at least be 8 characters',
            'required': 'Please provide a password'
        }
    )


    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # Method to validate user password
    def validate_password(self, data):
        # Pattern to check if password is alphanumeric
        alphanumeric = re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d.*)(?=.*\W.*)[a-zA-Z0-9\S]{8,15}$", data)

        # If the password is not Alphanumeric raise validation error
        if not alphanumeric:
            raise serializers.ValidationError(
                {"message": "Password not Strong Enough," +
                    "It should be Alphanumeric and Contain special characters"}
            )
        return data


    def create(self, validated_data):
        # create a new user
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # token when user logs in
    token = serializers.CharField(max_length=1028, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        # email not provided
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # password not provided
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # Authenticate User, `we set username to email in our model`
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        return {
            'email': user.email,
            'token': user.token
        }