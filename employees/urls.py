from django.urls import path, include
from . import views

urlpatterns = [
    path("employees/", views.employee_index, name="employee_index"),
    path("employees/users", views.employee_users, name="employee_users"),
    path("employees/savings", views.employee_savings, name="employee_savings"),
    path("employees/transactions", views.employee_transactions, name="employee_transactions")
]