from django.db import models

class Savings(models.Model):
    type = models.CharField(max_length=20)
    citizen_id = models.CharField(max_length=12)
    address = models.CharField(max_length=100)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)