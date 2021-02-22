from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView

from .forms import RegisterForm, LoginForm, ApplicationForm, CompanyEditForm, VacancyEditForm
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


class MyCompanyCreateView(View):
    def get(self, request):
        # TODO: попробовать создать форму, заполнить ее пустотой и отправить в рендер?
        Company.objects.create(
            name='',
            owner=request.user,
            location='',
            description='',
            employee_count=0,
        )
        return redirect('my_company')


class MyCompanyView(View):
    def get(self, request):
        user = request.user
        user_company = Company.objects.filter(owner=user).first()  # TODO: get_or_404
        if user_company:
            form = CompanyEditForm(instance=user_company)
            return render(request, 'company-edit.html', context={'form': form})
        else:
            return render(request, 'company-create.html')

    def post(self, request):
        user = request.user
        user_company = Company.objects.filter(owner=user).first()
        form = CompanyEditForm(request.POST, request.FILES, instance=user_company)
        if form.is_valid():
            application = form.save(commit=False)
            application.owner_id = request.user.id
            application.save()
            return render(request, 'company-edit.html', context={'form': form, 'is_updated': True})  #TODO: is updated попрбовать через messages
        return render(request, 'company-edit.html', context={'form': form})


class MyCompanyVacancyCreateView(View):
    def get(self, request):
        # TODO: попробовать создать форму, заполнить ее пустотой и отправить в рендер?
        vacancy = Vacancy.objects.create(
            title='',
            company=request.user.company.first(),
            description='',
            salary_min=0,
            salary_max=0,
        )
        return redirect('my_company_vacancy_edit', vacancy.id)


class MyCompanyVacanciesView(View):
    def get(self, request):
        user = request.user
        user_company = Company.objects.filter(owner=user).first()   # TODO: get_or_404
        user_vacancies = Vacancy.objects.filter(company=user_company)
        if user_vacancies:
            # form = CompanyEditForm(instance=user_company)
            return render(request, 'vacancies-list.html', context={'vacancies': user_vacancies})
        else:
            return render(request, 'vacancy-create.html')

    # def post(self, request):
    #     user = request.user
    #     user_company = Company.objects.filter(owner=user).first()
    #     form = CompanyEditForm(request.POST, request.FILES, instance=user_company)
    #     if form.is_valid():
    #         application = form.save(commit=False)
    #         application.owner_id = request.user.id
    #         application.save()
    #         return render(request, 'company-edit.html', context={'form': form, 'is_updated': True})
    #     return render(request, 'company-edit.html', context={'form': form})


class MyCompanyVacancyEdit(View):
    def get(self, request, pk):
        vacancy = Vacancy.objects.filter(id=pk).first()  # TODO: get_or_404
        if vacancy:
            form = VacancyEditForm(instance=vacancy)
            return render(request, 'test.html', context={'form': form})

    def post(self, request, pk):
        vacancy = Vacancy.objects.filter(id=pk).first()  # TODO: get_or_404
        form = VacancyEditForm(request.POST, instance=vacancy)
        if form.is_valid():
            application = form.save(commit=False)
            # application.owner_id = request.user.id
            application.save()
            return render(request, 'test.html', context={'form': form, 'is_updated': True})  #TODO: is updated попрбовать через messages
        return render(request, 'test.html', context={'form': form})


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
