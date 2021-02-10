from django.urls import path

from vacancies.views import ListVacanciesView, DetailVacancyView, custom_handler500, custom_handler404


urlpatterns = [
    path('', ListVacanciesView.as_view(), name='vacancies'),
    path('cat/<str:category>/', ListVacanciesView.as_view(), name='category'),
    path('<int:pk>/', DetailVacancyView.as_view(), name='vacancy'),
]

handler404 = custom_handler404
handler500 = custom_handler500
