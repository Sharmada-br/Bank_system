from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL
ACCOUNT_TYPES = [
    ('Savings', 'Savings'),
    ('Current', 'Current'),
    ('Salary', 'Salary'),
]

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    bank_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20)  
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)