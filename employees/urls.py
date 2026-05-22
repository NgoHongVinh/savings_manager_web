from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.employee_index, name="employee_index"),
    path("users/", views.employee_users, name="employee_users"),
    path("savings/", views.employee_savings, name="employee_savings"),
    path("transactions/", views.employee_transactions, name="employee_transactions")
]