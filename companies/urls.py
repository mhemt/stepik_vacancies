from django.urls import path

from companies.views import DetailCompanyView, ListCompaniesView


urlpatterns = [
    path('', ListCompaniesView.as_view(), name='companies'),
    path('<int:pk>', DetailCompanyView.as_view(), name='company'),
]
