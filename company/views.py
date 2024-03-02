from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import TemplateView, View
from .models import Company, Vacancy, Speciality, Application, Resume
from .forms import ApplicationForm, SearchForm
from django.http import HttpResponseNotFound, HttpResponse


class MainView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['specialities'] = (
            Speciality.objects.all()
            .annotate(vacancy_count=Count('vacancies'))
        )
        context['companies'] = (
            Company.objects
            .order_by('-company_count')[:8]
            .annotate(company_count=Count('vacancies'))
        )
        context['form'] = SearchForm
        return context


class DetailCompany(TemplateView):
    template_name = 'main/detail_company.html'

    def get_context_data(self, **kwargs):
        context = super(DetailCompany, self).get_context_data(**kwargs)
        context['company'] = get_object_or_404(Company, pk=kwargs['pk'])
        context['vacancies'] = (
            Vacancy.objects
            .filter(company=kwargs['pk']))
        return context


class CompanyVacancies(TemplateView):
    template_name = 'main/company_vacancies.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyVacancies, self).get_context_data(**kwargs)
        context['company'] = get_object_or_404(Company, pk=kwargs['pk'])
        context['vacancies'] = (
            Vacancy.objects
            .filter(company=kwargs['pk'])
            .order_by('title')
        )
        return context


class DetailVacancy(View):
    def get(self, request, pk):
        vacancy = get_object_or_404(Vacancy, pk=pk)
        form = ApplicationForm
        context = {
            'vacancy': vacancy,
            'form': form,
        }
        return render(request, 'main/detail_vacancy.html', context=context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = User(request.user)
        else:
            messages.info(request, 'Авторизуйтесь для того чтобы оставить отклик')
            return redirect('/login/')
        form = ApplicationForm(request.POST)
        vacancy = get_object_or_404(Vacancy, pk=kwargs['pk'])
        if form.is_valid():
            username = form.cleaned_data['username']
            phone = form.cleaned_data['phone']
            letter = form.cleaned_data['letter']
            Application.objects.create(
                username=username,
                phone=phone,
                letter=letter,
                user=user.pk,
                vacancy=vacancy,
            )
            return redirect('/send/success/')
        return render(request, 'main/detail_vacancy.html', context={'form': form, 'vacancy': vacancy})


class DetailSpeciality(TemplateView):
    template_name = 'main/detail_vacancies.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DetailSpeciality, self).get_context_data(**kwargs)
        speciality = Speciality.objects.get(code=kwargs['code'])
        context['vacancies'] = Vacancy.objects \
            .filter(speciality=speciality.id) \
            .select_related('company') \
            .order_by('title')
        context['spec_title'] = speciality.title
        return context


class VacanciesView(TemplateView):
    template_name = 'main/all_vacancies.html'

    def get_context_data(self, **kwargs):
        context = super(VacanciesView, self).get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.all()\
            .order_by('title')\
            .select_related('company')
        return context


class CompaniesView(TemplateView):
    template_name = 'main/all_companies.html'

    def get_context_data(self, **kwargs):
        context = super(CompaniesView, self).get_context_data(**kwargs)
        context['companies'] = (
            Company.objects.all().annotate(company_count=Count('vacancies')).order_by('title')
        )
        return context


class SentView(TemplateView):
    template_name = 'main/sent.html'


class SearchView(View):
    def get(self, request):
        data = request.GET.get('data', False)
        if data:
            vacancies = Vacancy.objects \
                .filter(Q(title__icontains=data) | Q(skills__icontains=data)) \
                .order_by('title')\
                .select_related('company')
        else:
            vacancies = Vacancy.objects.all().select_related('company')
        context = {
            'vacancies': vacancies,
            'form': SearchForm(request.GET),
        }
        return render(request, 'main/search.html', context=context)


class ApplicationResumeView(TemplateView):
    template_name = 'resume/user_resume.html'

    def get_context_data(self, **kwargs):
        context = super(ApplicationResumeView, self).get_context_data(**kwargs)
        user_app = Application.objects.get(pk=kwargs['pk'])
        try:
            context['resume'] = Resume.objects.get(user=user_app.user)
            context['exist'] = False
            return context
        except ObjectDoesNotExist:
            context['exist'] = True
            return context


class OpenResumesView(TemplateView):
    template_name = 'main/all_resume.html'

    def get_context_data(self, **kwargs):
        context = super(OpenResumesView, self).get_context_data(**kwargs)
        context['resumes'] = Resume.objects.all().order_by('name')
        return context


class DetailOpenResume(View):
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk)
        context = {
            'resume': resume
        }
        return render(request, 'main/detail_resume.html', context=context)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена 404</h1>')


def server_error(request):
    return HttpResponse(request, '<h1>Ой, что-то сломалось</h1>')
