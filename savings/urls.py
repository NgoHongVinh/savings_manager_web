from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.saving_plans, name="saving_plans"),
]
