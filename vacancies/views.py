from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View, CreateView

from .forms import RegisterForm, LoginForm, ApplicationForm, CompanyEditForm, VacancyEditForm, ResumeEditForm
from .models import Company, Specialty, Vacancy, Application, Resume


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.annotate(Count('vacancies'))
        companies = Company.objects.annotate(Count('vacancies'))

        context = {
            'specialties': specialties,
            'companies': companies,
        }
        return render(request, 'index.html', context=context)


class VacanciesView(View):
    def get(self, request, category=None):
        vacancies = Vacancy.objects.prefetch_related('skills').select_related('company', 'specialty').all()
        category_name = None

        if category:
            vacancies = vacancies.filter(specialty__code=category)
            category_name = get_object_or_404(Specialty, code=category).title

        context = {
            'vacancies': vacancies,
            'category_name': category_name,
        }
        return render(request, 'vacancies.html', context=context)


@method_decorator(login_required, 'post')
class VacancyView(View):
    def get(self, request, pk):
        vacancy = get_object_or_404(
            Vacancy.objects.prefetch_related('skills').select_related('company', 'specialty'),
            id=pk,
        )

        context = {
            'vacancy': vacancy,
            'form': ApplicationForm,
        }
        return render(request, 'vacancy.html', context=context)

    def post(self, request, pk):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user_id = request.user.id
            application.vacancy_id = pk
            application.save()
            return redirect('application_sent', pk=pk)
        return render(request, 'vacancy.html', context={'form': form})


class CompanyView(View):
    def get(self, request, pk):
        company = get_object_or_404(Company, id=pk)
        vacancies = Vacancy.objects.filter(company=company)\
            .prefetch_related('skills')\
            .select_related('company', 'specialty')

        context = {
            'company': company,
            'vacancies': vacancies,
        }
        return render(request, 'company.html', context=context)


class ApplicationSentView(View):
    def get(self, request, pk):
        return render(request, 'sent.html')


class MyCompanyCreateView(LoginRequiredMixin, View):
    def get(self, request):
        Company.objects.create(
            owner=request.user,
        )
        return redirect('my_company')


class MyCompanyView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_company = Company.objects.filter(owner=user).first()
        if user_company:
            form = CompanyEditForm(instance=user_company)
            return render(request, 'company-edit.html', context={'form': form})
        else:
            return render(request, 'company-create.html')

    def post(self, request):
        user = request.user
        user_company = get_object_or_404(Company, owner=user)
        form = CompanyEditForm(request.POST, request.FILES, instance=user_company)
        if form.is_valid():
            form.save()

            context = {
                'form': form,
                'is_updated': True,
            }
            return render(request, 'company-edit.html', context=context)
        return render(request, 'company-edit.html', context={'form': form})


class MyCompanyVacancyCreateView(LoginRequiredMixin, View):
    def get(self, request):
        vacancy = Vacancy.objects.create(
            company=request.user.company,
        )
        return redirect('my_company_vacancy_edit', vacancy.id)


class MyCompanyVacanciesView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_company = get_object_or_404(Company, owner=user)
        user_vacancies = Vacancy.objects.filter(company=user_company).prefetch_related('applications')
        if user_vacancies:
            return render(request, 'vacancies-list.html', context={'vacancies': user_vacancies})
        else:
            return render(request, 'vacancy-create.html')


class MyCompanyVacancyEdit(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = request.user
        vacancy = get_object_or_404(Vacancy, id=pk, company__owner__id=user.id)
        if vacancy:
            form = VacancyEditForm(instance=vacancy)
            applications = Application.objects.filter(vacancy=vacancy)

            context = {
                'form': form,
                'applications': applications,
            }
            return render(request, 'vacancy-edit.html', context=context)

    def post(self, request, pk):
        vacancy = get_object_or_404(Vacancy, id=pk)
        form = VacancyEditForm(request.POST, instance=vacancy)
        if form.is_valid():
            form.save()

            context = {
                'form': form,
                'is_updated': True,
            }
            return render(request, 'vacancy-edit.html', context=context)
        return render(request, 'vacancy-edit.html', context={'form': form})


class MyResumeCreateView(LoginRequiredMixin, View):
    def get(self, request):
        Resume.objects.create(
            owner=request.user,
        )
        return redirect('my_resume')


class MyResumeView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_resume = Resume.objects.filter(owner=user).select_related('specialty').first()
        if user_resume:
            form = ResumeEditForm(instance=user_resume)
            return render(request, 'resume-edit.html', context={'form': form})
        else:
            return render(request, 'resume-create.html')

    def post(self, request):
        user = request.user
        user_resume = get_object_or_404(Resume, owner=user)
        form = ResumeEditForm(request.POST, instance=user_resume)
        if form.is_valid():
            form.save()

            context = {
                'form': form,
                'is_updated': True,
            }
            return render(request, 'resume-edit.html', context=context)
        return render(request, 'resume-edit.html', context={'form': form})


class SearchView(View):
    def get(self, request):
        query = self.request.GET.get('s').strip()
        vacancies = (
            Vacancy.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
                           .prefetch_related('skills')
                           .select_related('company', 'specialty')
        )

        context = {
            'vacancies': vacancies,
            'query': query,
        }
        return render(request, 'search.html', context=context)


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    form_class = LoginForm
    template_name = 'login.html'


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = '/login'
    template_name = 'register.html'


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Простите извините! (404)')


def custom_handler500(request):
    return HttpResponseServerError('Ой, что то сломалось... Простите извините! (500)')
