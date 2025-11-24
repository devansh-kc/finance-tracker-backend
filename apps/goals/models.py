from django.db import models

# Create your models here.
userAuthConst = "auth.User"


class goals(models.Model):
    userUuid = models.ForeignKey(userAuthConst, on_delete=models.CASCADE)
    goalName = models.CharField(max_length=100)
    targetAmount = models.DecimalField(max_digits=10, decimal_places=2)
    currentSavings = models.DecimalField(max_digits=10, decimal_places=2)
