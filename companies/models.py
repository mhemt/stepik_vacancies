from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=30)
    logo = models.URLField(null=True, default='https://place-hold.it/100x60')
    description = models.TextField()
    employee_count = models.IntegerField()
