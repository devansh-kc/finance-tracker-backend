from rest_framework import serializers
from .models import User, UserSecurity, SecurityQuestion
from django.contrib.auth.password_validation import validate_password
from django.db import transaction


class UserSecuritySerilizer(serializers.ModelSerializer):
    class Meta:
        model = UserSecurity
        fields = ("question", "answer")

    def validate_question(self, value):
        if value in dict(UserSecurity.SecurityQuestion):
            raise serializers.ValidationError("Invalid security question.")
        return value


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    security = UserSecuritySerilizer(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "security",
        )
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "email": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        print("validated_data", validated_data)
        security_data = validated_data.pop("security")
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        UserSecurity.objects.create(
            user=user,
            question=security_data["question"],
            answer=security_data["answer"],
        )
