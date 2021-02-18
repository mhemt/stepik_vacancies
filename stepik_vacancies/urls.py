from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from vacancies.views import MainView, VacanciesView, VacancyView, DetailCompanyView, ApplicationSentView, \
    MyCompanyView, MyCompanyVacancies, MyCompanyVacancyEdit, LoginView, RegisterView, \
    custom_handler500, custom_handler404

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('cat/<str:category>/', VacanciesView.as_view(), name='category'),
    path('company/<int:pk>', DetailCompanyView.as_view(), name='company'),
    path('login/', LoginView.as_view(), name='login'),
    path('mycompany/', MyCompanyView.as_view(), name='mycompany'),
    path('mycompany/vacancies/', MyCompanyVacancies.as_view(), name='my_company_vacancies'),
    path('mycompany/vacancies/<int:pk>', MyCompanyVacancyEdit.as_view(), name='my_company_vacancy_edit'),
    path('register/', RegisterView.as_view(), name='register'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/<int:pk>/', VacancyView.as_view(), name='vacancy'),
    path('vacancies/<int:pk>/sent/', ApplicationSentView.as_view(), name='application_sent'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = custom_handler404
handler500 = custom_handler500
