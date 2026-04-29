from django.db import models
from django.conf import settings
import random

def generate_account_number():
    """Generates a random 10-digit account number."""
    return "".join([str(random.randint(0, 9)) for _ in range(10)])

class SavingAccount(models.Model):
    account_number = models.CharField(
        primary_key=True, 
        max_length=10, 
        default=generate_account_number, 
        editable=False
    )
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=50) # account holder's name'
    citizen_id = models.CharField(max_length=12)
    address = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saving_accounts')

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('OPEN', 'Account Opening'),
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdrawal'),
    ]

    account_number = models.CharField(max_length=10)
    name = models.CharField(max_length=50) # transaction maker's name
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    account = models.ForeignKey(SavingAccount, on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return f"{self.transaction_type}: {self.amount} on {self.timestamp}"