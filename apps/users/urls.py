from django.urls import path
from .views import SignupCreateAPI, SecurityQuestionsListView, LoginAPIView

app_name = "users"

urlpatterns = [
    path("signup/", SignupCreateAPI.as_view(), name="signup"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path(
        "security-questions/",
        SecurityQuestionsListView.as_view(),
        name="security-questions",
    ),
]
