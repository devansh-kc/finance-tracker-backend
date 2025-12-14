from django.urls import path
from .views import (
    SignupCreateAPI,
    SecurityQuestionsListView,
    LoginAPIView,
    LogoutAPIView,
    DeleteUserAPIView,
)

app_name = "users"

urlpatterns = [
    path("signup/", SignupCreateAPI.as_view(), name="signup"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("remove-user/<int:user_id>", DeleteUserAPIView.as_view(), name="delete"),
    path(
        "security-questions/",
        SecurityQuestionsListView.as_view(),
        name="security-questions",
    ),
]
