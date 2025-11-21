from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"  # Changed from 'users' to 'apps.users'
    verbose_name = "User Management"
