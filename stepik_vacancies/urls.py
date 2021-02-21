from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from vacancies.views import MainView, VacanciesView, VacancyView, CompanyView, ApplicationSentView, \
    MyCompanyView, MyCompanyVacancies, MyCompanyVacancyEdit, MyLoginView, RegisterView, \
    custom_handler500, custom_handler404, MyCompanyDummyView

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('cat/<str:category>/', VacanciesView.as_view(), name='category'),
    path('company/<int:pk>/', CompanyView.as_view(), name='company'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('mycompany/', MyCompanyView.as_view(), name='my_company'),
    path('mycompany/create/', MyCompanyDummyView.as_view(), name='my_company_create'),
    path('mycompany/vacancies/', MyCompanyVacancies.as_view(), name='my_company_vacancies'),
    path('mycompany/vacancies/create/', MyCompanyVacancies.as_view(), name='my_company_vacancy_create'),
    path('mycompany/vacancies/<int:pk>/', MyCompanyVacancyEdit.as_view(), name='my_company_vacancy_edit'),
    path('register/', RegisterView.as_view(), name='register'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/<int:pk>/', VacancyView.as_view(), name='vacancy'),
    path('vacancies/<int:pk>/sent/', ApplicationSentView.as_view(), name='application_sent'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = custom_handler404
handler500 = custom_handler500
