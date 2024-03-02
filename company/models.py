from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from Vacancies.settings import (
    MEDIA_COMPANY_IMAGE_DIR,
    MEDIA_SPECIALITY_IMAGE_DIR,
    MEDIA_RESUME_IMAGE_DIR,
    MEDIA_RESUME_IMAGE_DIR_default
)


class Vacancy(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название')
    speciality = models.ForeignKey('Speciality', related_name='vacancies', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', related_name='vacancies', on_delete=models.CASCADE)
    skills = models.CharField(max_length=150, verbose_name='Навыки')
    salary_min = models.PositiveSmallIntegerField(verbose_name='Мин зарплата')
    salary_max = models.PositiveSmallIntegerField(verbose_name='Макс зарплата')
    published = models.DateTimeField(default=datetime.now(), verbose_name='Опубликовано')

    def clean(self):
        if self.salary_min > self.salary_max:
            raise ValidationError('salary_max should be > salary_min')

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_vacancy', kwargs={"pk": self.pk})


class Company(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название')
    location = models.CharField(max_length=50, verbose_name='Город')
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, verbose_name='Лого')
    description = models.TextField(max_length=2000, verbose_name='Информация')
    employee_count = models.CharField(max_length=100, verbose_name='Кол-во сотрудников')
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Владелец', default=User)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_company', kwargs={"pk": self.pk})

    def get_vacancies_url(self):
        return reverse('company_vacancies', kwargs={"pk": self.pk})


class Speciality(models.Model):
    code = models.CharField(max_length=30, verbose_name='Код')
    title = models.CharField(max_length=30, verbose_name='Название')
    image = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_speciality', kwargs={"code": self.code})


# 10 лаба. Медиатор
class Application(models.Model):
    username = models.CharField(max_length=40, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    letter = models.TextField(max_length=1000, verbose_name='Письмо', default='', blank=True)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, verbose_name='Вакансия')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

    def __str__(self):
        return self.username


class Resume(models.Model):
    GRADE_CHOICES = [
        ('TR', 'Стажер'),
        ('JR', 'Джуноир'),
        ('MD', 'Мидл'),
        ('SR', 'Синьор'),
        ('TM', 'Тимлид'),
    ]
    STATUS_CHOICES = [
        ('NS', 'Не ищу работу'),
        ('SS', 'Рассматриваю предложения'),
        ('IS', 'Ищу работу'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=30, verbose_name='Имя')
    surname = models.CharField(max_length=30, verbose_name='Фамилия')
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='NS', verbose_name='Статус')
    salary = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Вознаграждение')
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, verbose_name='Специализация')
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES, default='TR', verbose_name='Квалификация')
    education = models.CharField(max_length=100, verbose_name='Образование')
    experience = models.CharField(max_length=100, verbose_name='Опыт работы')
    portfolio = models.URLField(max_length=200, verbose_name='Ссылка на портфолио')
    image = models.ImageField(
        upload_to=MEDIA_RESUME_IMAGE_DIR,
        default=MEDIA_RESUME_IMAGE_DIR_default,
        verbose_name='Изображение'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'

    def get_absolute_url(self):
        return reverse('detail_resume', kwargs={"pk": self.pk})
