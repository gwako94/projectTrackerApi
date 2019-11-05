from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import (
    UserRegisterSerializer
)

class RegisterView(CreateAPIView):
    """
    Register new User to the application
    """
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)

        # Validate date or raise exceptions
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_message = {
            "message": "Registration was successfull proceed to login"
        }

        return Response(response_message, status=status.HTTP_201_CREATED)
