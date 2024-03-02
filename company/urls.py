from django.urls import path

from .views import (
    MainView,
    DetailCompany,
    CompanyVacancies,
    DetailVacancy,
    VacanciesView,
    DetailSpeciality,
    SentView,
    SearchView,
    CompaniesView,
    OpenResumesView,
    DetailOpenResume,
)

urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('companies/', CompaniesView.as_view(), name='companies'),
    path('companies/<int:pk>/', DetailCompany.as_view(), name='detail_company'),
    path('companies/<int:pk>/vacancies', CompanyVacancies.as_view(), name='company_vacancies'),
    path('vacancies/<int:pk>/', DetailVacancy.as_view(), name='detail_vacancy'),
    path('vacancies/cat/<str:code>/', DetailSpeciality.as_view(), name='detail_speciality'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('send/success/', SentView.as_view(), name='sent'),
    path('search/', SearchView.as_view(), name='search'),
    path('resumes/', OpenResumesView.as_view(), name='resumes'),
    path('resumes/<int:pk>/', DetailOpenResume.as_view(), name='detail_resume'),
]
