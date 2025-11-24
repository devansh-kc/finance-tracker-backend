# Create your models here.
from django.db import models

userAuthConst = "auth.User"


class budget(models.Model):
    userUuid = models.ForeignKey(userAuthConst, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)

    monthlyLimit = models.DecimalField(max_digits=10, decimal_places=2)
