from django.db import models
from django.db.models import Sum, Q
from django.conf import settings
from django.utils.timezone import now
from decimal import Decimal
import random


def generate_account_number():
    """
    Generates unique random 10-digit account number.
    """

    while True:
        number = "".join([
            str(random.randint(0, 9))
            for _ in range(10)
        ])

        if not SavingAccount.objects.filter(
            account_number=number
        ).exists():
            return number


class SavingType(models.Model):

    name = models.CharField(max_length=50)

    duration_months = models.IntegerField(
        null=True,
        blank=True
    )

    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=4
    )

    is_active = models.BooleanField(default=True)

    is_flexible = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        old_rate = None

        if self.pk:
            old_rate = SavingType.objects.filter(
                pk=self.pk
            ).values_list(
                "interest_rate",
                flat=True
            ).first()

        super().save(*args, **kwargs)

        open_row = self.rate_history.filter(
            effective_to__isnull=True
        ).order_by(
            "-effective_from"
        ).first()

        if open_row is None:

            SavingTypeRateHistory.objects.create(
                saving_type=self,
                interest_rate=self.interest_rate,
                effective_from=now().date(),
                effective_to=None,
            )

            return

        if old_rate is not None and old_rate != self.interest_rate:

            today = now().date()

            open_row.effective_to = today

            open_row.save(
                update_fields=["effective_to"]
            )

            SavingTypeRateHistory.objects.create(
                saving_type=self,
                interest_rate=self.interest_rate,
                effective_from=today,
                effective_to=None,
            )

    def __str__(self):
        return self.name


class SavingTypeRateHistory(models.Model):

    saving_type = models.ForeignKey(
        SavingType,
        on_delete=models.CASCADE,
        related_name="rate_history"
    )

    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=4
    )

    effective_from = models.DateField()

    effective_to = models.DateField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["effective_from"]

    def __str__(self):

        end = self.effective_to or "present"

        return (
            f"{self.saving_type.name}: "
            f"{self.interest_rate}% "
            f"({self.effective_from} -> {end})"
        )


class SavingAccount(models.Model):

    account_number = models.CharField(
        primary_key=True,
        max_length=10,
        default=generate_account_number,
        editable=False
    )

    name = models.CharField(max_length=50)

    citizen_id = models.CharField(max_length=12)

    address = models.CharField(max_length=100)

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Snapshot interest rate
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=4
    )

    start_date = models.DateField(
        auto_now_add=True
    )

    maturity_date = models.DateField(
        null=True,
        blank=True
    )

    interest_last_applied_on = models.DateField(
        null=True,
        blank=True
    )

    saving_type = models.ForeignKey(
        SavingType,
        on_delete=models.PROTECT,
        related_name="accounts"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="saving_accounts"
    )

    def deposit(self, amount):

        amount = Decimal(amount)

        balance_before = self.balance

        self.balance += amount
        self.save()

        Transaction.objects.create(
            account=self,
            account_number=self.account_number,
            name=self.name,
            transaction_type="DEPOSIT",
            balance_before=balance_before,
            amount=amount,
            balance_after=self.balance
        )

    def withdraw(self, amount):

        amount = Decimal(amount)

        if amount > self.balance:
            raise ValueError("Insufficient balance")

        balance_before = self.balance

        self.balance -= amount
        self.save()

        Transaction.objects.create(
            account=self,
            account_number=self.account_number,
            name=self.name,
            transaction_type="WITHDRAW",
            balance_before=balance_before,
            amount=amount,
            balance_after=self.balance
        )

    def __str__(self):
        return f"{self.account_number} - {self.name}"


class Transaction(models.Model):

    TRANSACTION_TYPES = [
        ("OPEN", "Account Opening"),
        ("DEPOSIT", "Deposit"),
        ("WITHDRAW", "Withdrawal"),
        ("CLOSE", "Account Closing"),
    ]

    account_number = models.CharField(
        max_length=10
    )

    name = models.CharField(
        max_length=50
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES
    )

    balance_before = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )

    balance_after = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    account = models.ForeignKey(
        SavingAccount,
        null=True,
        on_delete=models.SET_NULL,
        related_name="transactions"
    )

    @classmethod
    def statistics(cls):

        total_income = cls.objects.filter(
            transaction_type__in=[
                "OPEN",
                "DEPOSIT"
            ]
        ).aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0")

        total_expense = cls.objects.filter(
            transaction_type__in=[
                "WITHDRAW",
                "CLOSE"
            ]
        ).aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0")

        difference = (
            total_income - total_expense
        )

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "difference": difference
        }

    @classmethod
    def daily_statistics(cls, date):

        total_income = cls.objects.filter(
            timestamp__date=date,
            transaction_type__in=[
                "OPEN",
                "DEPOSIT"
            ]
        ).aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0")

        total_expense = cls.objects.filter(
            timestamp__date=date,
            transaction_type__in=[
                "WITHDRAW",
                "CLOSE"
            ]
        ).aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0")

        difference = (
            total_income - total_expense
        )

        return {
            "date": date,
            "total_income": total_income,
            "total_expense": total_expense,
            "difference": difference
        }

    def __str__(self):

        return (
            f"{self.transaction_type}: "
            f"{self.amount} "
            f"on {self.timestamp}"
        )

