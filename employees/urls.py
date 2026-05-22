from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.employee_dashboard, name="employee_dashboard"),
    path("customers/", views.manage_customer, name="manage_customer"),
    path("staffs/", views.manage_staffs, name="manage_staffs"),
    path("savings/", views.manage_saving_accounts, name="manage_saving_accounts"),
    path("transactions/", views.manage_transactions, name="manage_transactions")
]