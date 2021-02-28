from datetime import date
from django.contrib.auth import get_user_model
from django.db import models

from stepik_vacancies.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALTY_IMAGE_DIR


class Company(models.Model):
    name = models.CharField(max_length=100)
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='company')
    location = models.CharField(max_length=30)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, default='company_images/130x80.gif')
    description = models.TextField(default='', blank=True)
    employee_count = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Specialty(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    picture = models.ImageField(upload_to=MEDIA_SPECIALTY_IMAGE_DIR)

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    specialty = models.ForeignKey(Specialty, null=True, blank=True, on_delete=models.SET_NULL, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.ManyToManyField(Skill, related_name='vacancies')
    description = models.TextField()
    salary_min = models.IntegerField(default=0)
    salary_max = models.IntegerField(default=0)
    published_at = models.DateField(default=date.today)

    def __str__(self):
        return self.title


class Application(models.Model):
    written_username = models.CharField(max_length=100)
    written_phone = models.CharField(max_length=20)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, related_name='applications', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name='applications', on_delete=models.CASCADE)

    def __str__(self):
        return self.written_username


class Resume(models.Model):
    STATUS_CHOICES = [
        ('not_looking', 'Не ищу работу'),
        ('taking_offers', 'Рассматриваю предложения'),
        ('looking', 'Ищу работу'),
    ]
    GRADE_CHOICES = [
        ('intern', 'Стажер'),
        ('junior', 'Джуниор'),
        ('middle', 'Миддл'),
        ('senior', 'Синьор'),
        ('lead', 'Лид'),
    ]

    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='resume')
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    salary = models.IntegerField(default=0)
    specialty = models.ForeignKey(Specialty, null=True, blank=True, on_delete=models.SET_NULL, related_name='resumes')
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    education = models.TextField()
    experience = models.TextField()
    portfolio = models.URLField(max_length=100, default='', blank=True)

    def __str__(self):
        return self.name
