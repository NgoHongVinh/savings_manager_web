from django.db import models
from django.conf import settings

class SavingAccount(models.Model):
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    citizen_id = models.CharField(max_length=12)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saving_accounts')

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('OPEN', 'Account Opening'),
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdrawal'),
    ]

    account = models.ForeignKey(SavingAccount, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type}: {self.amount} on {self.timestamp}"