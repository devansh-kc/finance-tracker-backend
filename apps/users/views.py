from rest_framework import generics
from .models import SecurityQuestion
from .serializers import UserSignupSerializer, SecurityQuestion
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import UserSignupSerializer, UserLoginSerializer
from rest_framework import status
from utils.responses import standard_response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class SignupCreateAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        serializer = UserSignupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user_token, created = Token.objects.get_or_create(user=user)
            return standard_response(
                success=True,
                message="User created successfully",
                data={"user": user, "userToken": user_token},
                status_code=status.HTTP_201_CREATED,
            )
        else:
            return standard_response(
                success=False,
                message="Validation failed",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class SecurityQuestionsListView(APIView):
    """
    API endpoint to get all available security questions
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        questions = [
            {"value": choice[0], "label": choice[1]}
            for choice in SecurityQuestion.choices
        ]
        return Response({"questions": questions}, status=status.HTTP_200_OK)


class LoginAPIView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            print("serializer is valid")
            user = serializer.validated_data.get("user")
            token, created = Token.objects.get_or_create(user=user)
            return standard_response(
                success=True,  # Should be True on success!
                message="Login successful",
                data={"token": token.key, "user": user},
                status_code=status.HTTP_200_OK,
            )
        else:
            return standard_response(
                success=False,
                message=serializer.error_messages,
                errors=serializer.errors,
                status_code=status.HTTP_403_FORBIDDEN,
            )
