from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.views.generic import View

from vacancies.models import Specialty, Skill, Vacancy
from companies.models import Company


class VacanciesView(View):
    def get(self, request, category=None):
        vacancies = Vacancy.objects.all()
        category_name = None

        if category:
            vacancies = Vacancy.objects.filter(specialty__code=category)
            category_name = Specialty.objects.filter(code=category).first().title

        context = {
            'vacancies': vacancies,
            'category_name': category_name,
        }
        return render(request, 'vacancies/vacancies.html', context)


class VacancyView(View):
    def get(self, request, pk):
        vacancy = Vacancy.objects.filter(id=pk).first()

        context = {
            'vacancy': vacancy,
        }
        return render(request, 'vacancies/vacancy.html', context)


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.all()
        companies = Company.objects.all()

        context = {
            'specialties': specialties,
            'companies': companies,
        }
        return render(request, 'index.html', context)


def main_view(request):
    return render(request, 'index.html')


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Простите извините!')


def custom_handler500(request):
    return HttpResponseServerError('Ой, что то сломалось... Простите извините!')
