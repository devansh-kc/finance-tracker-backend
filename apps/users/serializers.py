from rest_framework import serializers
from .models import UserSecurity, SecurityQuestion
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "date_joined"]
        # Or use fields = '__all__' for all fields
        # Use exclude = ['password'] to exclude sensitive fields


class UserSecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSecurity
        fields = ("question", "answer")

    def validate_question(self, value):
        if value not in dict(SecurityQuestion.choices):
            raise serializers.ValidationError("Invalid security question.")
        return value

    def validate_answer(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Security answer must be at least 3 characters long."
            )
        return value.strip()


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    security = UserSecuritySerializer(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "security",
        )
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "email": {"required": True},
        }

    def validate_email(self, value):
        normalized_email = value.lower().strip()
        if User.objects.filter(email__iexact=normalized_email).exists():
            raise serializers.ValidationError("Email address already exists.")
        return normalized_email

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    @transaction.atomic
    def create(self, validated_data):

        try:

            security_data = validated_data.pop("security")
            user = User.objects.create_user(**validated_data)
            UserSecurity.objects.create(
                user=user,
                question=security_data["question"],
                answer=security_data["answer"],
            )
            return user
        except Exception as error:
            print(error)
            raise serializers.ValidationError(
                "An error occurred while creating the user. Please try again.", error
            )


class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    "User doesnt exitsts By the provided email.", code="authorization"
                )
            if not user.check_password(password):
                raise serializers.ValidationError(
                    "Incorrect password", code="authorization"
                )
            if not user.is_active:
                raise serializers.ValidationError(
                    "User account is disabled.", code="authorization"
                )
            attrs["user"] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".', code="authorization"
            )
