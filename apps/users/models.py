from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.


class SecurityQuestion(models.TextChoices):
    MOTHER_MAIDEN_NAME = "mother_maiden_name", "What is your mother's maiden name?"
    FIRST_PET_NAME = "first_pet_name", "What was the name of your first pet?"
    BIRTH_CITY = "birth_city", "In which city were you born?"
    FAVORITE_TEACHER = "favorite_teacher", "Who was your favorite teacher?"
    FAVORITE_BOOK = "favorite_book", "What is your favorite book?"
    FAVORITE_FOOD = "favorite_food", "What is your favorite food?"
    CHILDHOOD_NICKNAME = "childhood_nickname", "What was your childhood nickname?"
    FIRST_SCHOOL_NAME = "first_school_name", "What was the name of your first school?"
    FAVORITE_MOVIE = "favorite_movie", "What is your favorite movie?"
    DREAM_JOB = "dream_job", "What was your dream job as a child?"
    FIRST_CAR = "first_car", "What was the make of your first car?"
    FAVORITE_SPORT = "favorite_sport", "What is your favorite sport?"
    FAVORITE_VACATION_PLACE = (
        "favorite_vacation_place",
        "What is your favorite vacation place?",
    )
    BEST_FRIEND_NAME = "best_friend_name", "What is the first name of your best friend?"
    FAVORITE_COLOR = "favorite_color", "What is your favorite color?"
    FAVORITE_SUBJECT = "favorite_subject", "What was your favorite subject in school?"
    GRANDMOTHER_FIRST_NAME = (
        "grandmother_first_name",
        "What is your grandmother’s first name?",
    )
    CHILDHOOD_STREET = "childhood_street", "What street did you grow up on?"
    FAVORITE_SINGER = "favorite_singer", "Who is your favorite singer or musician?"
    FAVORITE_GAME = "favorite_game", "What is your favorite game?"


class UserSecurity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="security")
    question = models.CharField(max_length=50, choices=SecurityQuestion.choices)
    answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Security Question"
        verbose_name_plural = "User Security Questions"

    def set_answer(self, raw_answer):
        """Hash and store the security answer (case-insensitive)"""
        self.answer = make_password(raw_answer.lower().strip())

    def check_answer(self, raw_answer):
        """Verify the security answer (case-insensitive)"""
        return check_password(raw_answer.lower().strip(), self.answer)

    def __str__(self):
        return f"{self.user.email} - {self.get_question_display()}"
