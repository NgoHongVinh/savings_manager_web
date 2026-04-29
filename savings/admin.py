from django.contrib import admin
from models import *

@admin.register(SavingType)
class SavingAdmin(admin.ModelAdmin):
    list_display = ("name", "duration_months", "interest_rate", "is_active")

@admin.register(SavingAccount)
class SavingAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "name", "citizen_id", "address", "balance", "created_at")

@admin.register(Transaction)
class SavingAdmin(admin.ModelAdmin):
    list_display = ("account_number", "name", "transaction_type", "amount", "timestamp")