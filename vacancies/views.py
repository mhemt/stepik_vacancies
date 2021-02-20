from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView

from .forms import RegisterForm, LoginForm, ApplicationForm, CompanyEditForm
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
            'form': ApplicationForm,
        }
        return render(request, 'vacancy.html', context)

    def post(self, request, pk):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user_id = request.user.id
            application.vacancy_id = pk
            application.save()
            return redirect('application_sent', pk=pk)
        return render(request, 'vacancy.html', context={'form': form})


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.all()
        companies = Company.objects.all()

        context = {
            'specialties': specialties,
            'companies': companies,
        }
        return render(request, 'index.html', context)


class CompanyView(View):
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
        user = request.user
        user_company = Company.objects.filter(owner=user).first()
        if user_company:
            print(user.company.name)
            form = CompanyEditForm(instance=user_company)
            return render(request, 'company-edit.html', context={'from': form})
        else:
            return render(request, 'company-create.html')

    def post(self, request):
        form = CompanyEditForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user_id = request.user.id
            application.save()
            # return redirect('mycompany')
        return render(request, 'company-edit.html', context={'form': form})


class MyCompanyDummyView(View):
    def get(self, request):
        company = Company.objects.create(
            name='',
            owner=request.user,
            location='',
            logo='',
            description='',
            employee_count=0,
        )
        return redirect('mycompany')


class MyCompanyVacancies(View):
    def get(self, request):
        return render(request, 'vacancies-list.html')


class MyCompanyVacancyEdit(View):
    def get(self, request, pk):
        return render(request, 'vacancy-edit.html')


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    form_class = LoginForm
    template_name = 'login.html'


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = '/'
    template_name = 'register.html'


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Простите извините! (404)')


def custom_handler500(request):
    return HttpResponseServerError('Ой, что то сломалось... Простите извините! (500)')
