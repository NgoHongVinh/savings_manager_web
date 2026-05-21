from django.contrib import admin
from .models import CustomUser, Customer, Employee

admin.site.register(CustomUser)
admin.site.register(Customer)
admin.site.register(Employee)