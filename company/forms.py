from crispy_forms.bootstrap import FormActions, AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Vacancy, Company, Resume


class ApplicationForm(forms.Form):
    username = forms.CharField(max_length=40, label='Имя')
    phone = forms.CharField(max_length=11, label='Телефон')
    letter = forms.CharField(max_length=1500, widget=forms.Textarea, required=False, label='Письмо')

    class Meta:
        fields = ('username', 'phone', 'letter')


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ('title', 'location', 'logo', 'description', 'employee_count')


class VacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = ('title', 'speciality', 'skills', 'salary_min', 'salary_max')
        labels = {
            'title': 'Название вакансии',
            'speciality': 'Специализация',
            'skills': 'Навыки',
            'salary_min': 'Зарплата от',
            'salary_max': 'Зарплата до',
        }


class ResumeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = 'post'

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-6'
        self.helper.field_class = 'col-lg-6'
        self.helper.layout = Layout(
            Fieldset(
                'Личные данные:',
                AppendedText('name', '', placeholder="Ваше имя"),
                AppendedText('surname', '', placeholder="Ваша фамилия"),
                'grade',
                AppendedText('speciality', '', placeholder="Специализация"),
            ),
            Fieldset(
                '<hr>',
            ),
            Fieldset(
                'Остальное:',
                AppendedText('education', '', placeholder="Образовнаие"),
                AppendedText('experience', '', placeholder="Опыт работы"),
                AppendedText('status', '', placeholder="Готовность к работе"),
                AppendedText('salary', '', placeholder="Ваше вознограждение"),
                AppendedText('portfolio', '', placeholder="Ссылка на git"),
                AppendedText('image', '', placeholder="Ваша фотография"),
            ),
            FormActions(
                Submit('submit', 'Сохранить'),
            ),
        )

    class Meta:
        model = Resume
        fields = (
            'name',
            'surname',
            'status',
            'salary',
            'speciality',
            'grade',
            'education',
            'experience',
            'portfolio',
            'image',
        )
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'speciality': 'Специализация',
            'status': ' Статус',
            'grade': 'Квалификация',
            'education': 'Образование',
            'experience': 'Опыт работы',
            'portfolio': 'Портфолио',
            'image': 'Фотография',
        }


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Почта',
        }


class ChangePasswordForm(forms.Form):
    password_now = forms.CharField(widget=forms.PasswordInput(), label='Текущий пароль')
    password_new = forms.CharField(widget=forms.PasswordInput(), label='Новый пароль')

    class Meta:
        fields = ('password_now', 'password_new')


class SearchForm(forms.Form):
    data = forms.CharField(
        max_length=30,
        label='Поиск по вакансиям',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control w-100',
                'placeholder': 'Найти работу или стажировку',
                'aria-label': 'Найти работу или стажировку',
            },
        ))

    class Meta:
        fields = ('data',)
