from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from company.forms import CompanyForm, VacancyForm, ResumeForm, ProfileForm, ChangePasswordForm
from .forms import MyRegistrationForm
from django.shortcuts import render, redirect
from company.models import Company, Vacancy, Application, Resume


def check_company(request):
    try:
        Company.objects.get(owner=request.user.id)
        return redirect('/mycompany/')
    except ObjectDoesNotExist:
        return render(request, 'company/company_check.html')


def check_resume(request):
    try:
        Resume.objects.get(user=request.user.id)
        return redirect('/myresume/')
    except ObjectDoesNotExist:
        return render(request, 'resume/resume-check.html')


class MyRegistrationView(View):
    def get(self, request):
        return render(request, 'users/registration.html', context={'form': MyRegistrationForm})

    def post(self, request, *args, **kwargs):
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
        return render(request, 'users/registration.html', context={'form': form})


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'users/login.html'


@method_decorator(login_required, name='get')
class ProfileCompanyView(View):
    def get(self, request):
        try:
            company = Company.objects.get(owner=request.user.id)
            return render(request, 'company/company_edit.html', context={'form': CompanyForm(instance=company)})
        except ObjectDoesNotExist:
            return render(request, 'company/company_edit.html', context={'form': CompanyForm})

    def post(self, request, *args, **kwargs):
        form = CompanyForm(request.POST, request.FILES)
        user = self.request.user
        if form.is_valid():
            form_data = form.cleaned_data

            defaults = {**form_data}
            defaults['owner'] = user

            Company.objects.update_or_create(owner__id=user.id, defaults=defaults)
            messages.info(request, 'Компания обновлена')
            return redirect('/mycompany/')
        return render(request, 'company/company_edit.html', context={'form': form})


@method_decorator(login_required, name='get')
class ProfileVacanciesView(View):
    def get(self, request):
        try:
            company = Company.objects.get(owner=self.request.user.id)
            vacancies = Vacancy.objects.filter(company=company) \
                .annotate(app_count=Count('application'))\
                .order_by('title')\
                .select_related('company')
            context = {'vacancies': vacancies}
            return render(request, 'vacancy/vacancy-list.html', context=context)
        except ObjectDoesNotExist:
            return redirect('/profile/check/')


class ProfileVacanciesEdit(View):
    def get(self, request, pk):
        vacancy = Vacancy.objects.get(pk=pk)
        applications = Application.objects.filter(vacancy=vacancy)
        context = {
            'title': vacancy.title,
            'form': VacancyForm(instance=vacancy),
            'applications': applications,
        }
        return render(request, 'vacancy/vacancy_edit.html', context=context)

    def post(self, request, *args, **kwargs):
        form = VacancyForm(request.POST)
        company = Company.objects.get(owner=self.request.user.id)
        if form.is_valid():
            form = form.cleaned_data
            Vacancy.objects.update_or_create(defaults=form, company=company)
            messages.info(request, 'Ваканися обновлена')
            return redirect('/mycompany/vacancies/')
        return render(request, 'vacancy/vacancy_edit.html', context={'form': form})


@method_decorator(login_required, name='get')
class ProfileVacanciesCreate(View):
    def get(self, request):
        return render(request, 'vacancy/vacancy_create.html', context={'form': VacancyForm})

    def post(self, request, *args, **kwargs):
        form = VacancyForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            speciality = form.cleaned_data['speciality']
            company = Company.objects.get(owner=self.request.user.id)
            skills = form.cleaned_data['skills']
            salary_min = form.cleaned_data['salary_min']
            salary_max = form.cleaned_data['salary_max']
            Vacancy.objects.create(
                title=title,
                speciality=speciality,
                company=company,
                skills=skills,
                salary_min=salary_min,
                salary_max=salary_max,
            )
            return redirect('/mycompany/vacancies/')
        return render(request, 'vacancy/vacancy_create.html', context={'form': form})


@method_decorator(login_required, name='get')
class ResumeView(View):
    def get(self, request):
        try:
            resume = Resume.objects.get(user=request.user.id)
            return render(request, 'resume/resume-edit.html', context={'form': ResumeForm(instance=resume)})
        except ObjectDoesNotExist:
            return render(request, 'resume/resume-edit.html', context={'form': ResumeForm})

    def post(self, request, *args, **kwargs):
        form = ResumeForm(request.POST)
        if form.is_valid():
            defaults = form.cleaned_data
            Resume.objects.update_or_create(defaults=defaults, user=request.user)
            messages.info(request, 'Резюме обновлено')
            return redirect('/myresume/')
        return render(request, 'resume/resume-edit.html', context={'form': form})


@method_decorator(login_required, name='get')
class ProfileView(View):
    def get(self, request):
        return render(request, 'users/profile.html', context={'form': ProfileForm(instance=request.user)})

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            messages.info(request, 'Профиль обновлен')
        return render(request, 'users/profile.html', context={'form': form})


@method_decorator(login_required, name='get')
class ChangePasswordView(View):
    def get(self, request):
        return render(request, 'users/change_password.html', context={'form': ChangePasswordForm})

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            password_now = form.cleaned_data['password_now']
            if user.check_password(password_now):
                password_new = form.cleaned_data['password_new']
                user.set_password(password_new)
                user.save()
                messages.info(request, 'Пароль успешно обновлен')
                return redirect('/login/')
            form.add_error('password_now', 'Неверный пароль!')
        return render(request, 'users/change_password.html', context={'form': form})
