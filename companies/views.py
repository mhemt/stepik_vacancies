from django.shortcuts import render
from django.views.generic import ListView, View

from vacancies.models import Vacancy
from companies.models import Company


class ListCompaniesView(ListView):
    ...


class DetailCompanyView(View):
    def get(self, request, pk):
        company = Company.objects.get(id=pk)
        vacancies = Vacancy.objects.filter(company=company)

        context = {
            'company': company,
            'vacancies': vacancies,
        }
        return render(request, 'companies/company.html', context)
