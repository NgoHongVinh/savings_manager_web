from django.contrib import admin
from .models import *

admin.site.register(SavingType)
admin.site.register(SavingPlan)
admin.site.register(SavingTypeRateHistory)
admin.site.register(Transaction)