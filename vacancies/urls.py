from django.urls import path

from vacancies.views import VacanciesView, VacancyView


urlpatterns = [
    path('', VacanciesView.as_view(), name='vacancies'),
    path('cat/<str:category>/', VacanciesView.as_view(), name='category'),
    path('<int:pk>/', VacancyView.as_view(), name='vacancy'),
]
