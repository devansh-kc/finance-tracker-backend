from django.db import models

# Create your models here.
userAuthConst = "auth.User"


class TransactionType(models.TextChoices):
    INCOME = "Income"
    EXPENSE = "Expense"


class UserTransations(models.Model):
    transactionType = models.CharField(
        max_length=100, choices=TransactionType.choices, default=TransactionType.INCOME
    )
    userUuid = models.ForeignKey(userAuthConst, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    Date = models.DateField(auto_now=True)
    note = models.CharField(max_length=255)
