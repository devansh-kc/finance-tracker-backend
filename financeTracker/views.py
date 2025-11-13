from rest_framework import generics
from .models import User
from .serializers import UserSerilizer
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


class SignupCreateAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        print("self", self)
        print("request", request)
        return Response({"message": "GET request to signup page"})

    def post(self, request):
        print("self", self)
        print("request", request)
        return HttpResponse("Welcome to the signuppage!")


def index(request):
    return HttpResponse("Welcome to the homepage!")
