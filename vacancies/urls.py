from django.urls import path

from vacancies.views import VacanciesView, VacancyView, custom_handler500, custom_handler404


urlpatterns = [
    path('', VacanciesView.as_view(), name='vacancies'),
    path('cat/<str:category>/', VacanciesView.as_view(), name='category'),
    path('<int:pk>/', VacancyView.as_view(), name='vacancy'),
]

handler404 = custom_handler404
handler500 = custom_handler500
