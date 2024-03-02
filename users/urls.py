from django.contrib.auth.views import LogoutView
from django.urls import path

from company.views import ApplicationResumeView
from .views import (
    MyLoginView,
    MyRegistrationView,
    ProfileCompanyView,
    ProfileVacanciesView,
    ProfileVacanciesEdit,
    ProfileVacanciesCreate,
    check_company,
    check_resume,
    ResumeView,
    ProfileView,
    ChangePasswordView,
)

urlpatterns = [
    path('profile/check/', check_company, name='profile_check'),
    path('resume/check/', check_resume, name='resume_check'),
    path('myprofile/', ProfileView.as_view(), name='profile'),
    path('profile/change/password/', ChangePasswordView.as_view(), name='change_password'),
    path('registration/', MyRegistrationView.as_view(), name='reg'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('myresume/', ResumeView.as_view(), name='resume'),
    path('mycompany/', ProfileCompanyView.as_view(), name='profile_company'),
    path('mycompany/vacancies/', ProfileVacanciesView.as_view(), name='profile_vacancies'),
    path('mycompany/vacancies/<int:pk>/', ProfileVacanciesEdit.as_view(), name='edit_vacancy'),
    path('mycompany/vacancies/create/', ProfileVacanciesCreate.as_view(), name='create_vacancy'),
    path('resume/<int:pk>/', ApplicationResumeView.as_view(), name='user_resume'),
]
