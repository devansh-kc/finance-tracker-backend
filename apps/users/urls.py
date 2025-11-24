from django.urls import path
from .views import SignupCreateAPI, SecurityQuestionsListView

app_name = "users"

urlpatterns = [
    path("signup/", SignupCreateAPI.as_view(), name="signup"),
    path(
        "security-questions/",
        SecurityQuestionsListView.as_view(),
        name="security-questions",
    ),
]
