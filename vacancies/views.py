from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.views.generic import View

from .models import Company, Specialty, Vacancy


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
        return render(request, 'vacancies.html', context)


class VacancyView(View):
    def get(self, request, pk):
        vacancy = Vacancy.objects.get(id=pk)

        context = {
            'vacancy': vacancy,
        }
        return render(request, 'vacancy.html', context)


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.all()
        companies = Company.objects.all()

        context = {
            'specialties': specialties,
            'companies': companies,
        }
        return render(request, 'index.html', context)


class DetailCompanyView(View):
    def get(self, request, pk):
        company = Company.objects.get(id=pk)
        vacancies = Vacancy.objects.filter(company=company)

        context = {
            'company': company,
            'vacancies': vacancies,
        }
        return render(request, 'company.html', context)


class ApplicationSentView(View):
    def get(self, request, pk):
        return render(request, 'sent.html')


class MyCompanyView(View):
    def get(self, request):
        # return render(request, 'company-create.html')
        return render(request, 'company-edit.html')


class MyCompanyVacancies(View):
    def get(self, request):
        return render(request, 'vacancies-list.html')


class MyCompanyVacancyEdit(View):
    def get(self, request, pk):
        return render(request, 'vacancy-edit.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Простите извините! (404)')


def custom_handler500(request):
    return HttpResponseServerError('Ой, что то сломалось... Простите извините! (500)')
