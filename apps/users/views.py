from rest_framework import generics
from .models import SecurityQuestion
from .serializers import (
    UserSignupSerializer,
    SecurityQuestion,
    UserSignupSerializer,
    UserLoginSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from utils.responses import standard_response
from utils.cookie_function import set_cookie_data, delete_cookie_data
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated


class SignupCreateAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        serializer = UserSignupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user_token, created = Token.objects.get_or_create(user=user)
            response = standard_response(
                success=True,
                message="User created successfully",
                data={"user": serializer.data, "userToken": user_token.key},
                status_code=status.HTTP_201_CREATED,
            )
            set_cookie_data(
                response=response,
                key="auth_token",
                value=user_token.key,
                max_age=3600 * 24 * 7,  # Cookie expires in 7 days (in seconds)
            )
            return response

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
            user = serializer.validated_data.get("user")
            token, created = Token.objects.get_or_create(user=user)

            response = standard_response(
                success=True,  # Should be True on success!
                message="Login successful",
                data={"token": token.key},
                status_code=status.HTTP_200_OK,
            )
            set_cookie_data(
                response=response,
                key="auth_token",
                value=token.key,
                max_age=3600 * 24 * 7,  # Cookie expires in 7 days (in seconds)
            )
            return response
        else:
            return standard_response(
                success=False,
                message=serializer.error_messages,
                errors=serializer.errors,
                status_code=status.HTTP_403_FORBIDDEN,
            )


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Delete the token from database
            request.user.auth_token.delete()

            # Create response
            response = standard_response(
                success=True,
                message="User logged out successfully",
                data=None,
                status_code=status.HTTP_200_OK,
            )

            # Delete the cookie
            response.delete_cookie(
                key="auth_token",
                samesite="Lax",  # Should match the settings used when setting the cookie
            )

            return response

        except Exception as error:
            return standard_response(
                success=False,
                message="Logout failed",
                errors=str(error),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DeleteUserAPIView(APIView):
    pass
