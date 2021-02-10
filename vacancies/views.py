from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from vacancies.models import Specialty, Skill, Vacancy
from companies.models import Company


class ListVacanciesView(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'vacancies/vacancies.html'

    # def get_queryset(self):
    #     print(123124124, self.args)
    #     if self.args and self.args[0] == 'fluffy':
    #         fluffy = True
    #     else:
    #         fluffy = False
    #
    #     return Vacancy.objects.all()


# class ListVacanciesCatView(ListView):
#     model = Vacancy
#     context_object_name = 'vacancy'
#     template_name = 'vacancies.html'


class DetailVacancyView(DetailView):
    ...


class MainView(ListView):
    model = Specialty
    context_object_name = 'specialties'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        return context


def main_view(request):
    return render(request, 'index.html')


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Простите извините!')


def custom_handler500(request):
    return HttpResponseServerError('Ой, что то сломалось... Простите извините!')
