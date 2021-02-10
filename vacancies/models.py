from datetime import date
from django.db import models

from companies.models import Company


class Specialty(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    picture = models.URLField(default='https://place-hold.it/100x60')


class Skill(models.Model):
    name = models.CharField(max_length=30)


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.ManyToManyField(Skill, related_name='vacancies')
    description = models.TextField()
    salary_min = models.IntegerField(null=True)
    salary_max = models.IntegerField(null=True)
    published_at = models.DateField(default=date.today)
