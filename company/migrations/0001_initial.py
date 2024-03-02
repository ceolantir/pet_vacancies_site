# Generated by Django 3.0.4 on 2021-02-23 19:29

import datetime
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Название')),
                ('location', models.CharField(max_length=50, verbose_name='Город')),
                ('logo', models.ImageField(upload_to='company_images', verbose_name='Лого')),
                ('description', models.TextField(max_length=2000, verbose_name='Информация')),
                ('employee_count', models.CharField(max_length=100, verbose_name='Кол-во сотрудников')),
                ('owner', models.OneToOneField(default=django.contrib.auth.models.User,
                                               on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                               verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
            },
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, verbose_name='Код')),
                ('title', models.CharField(max_length=30, verbose_name='Название')),
                ('image', models.ImageField(upload_to='speciality_images', verbose_name='зображение')),
            ],
            options={
                'verbose_name': 'Специализация',
                'verbose_name_plural': 'Специализации',
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Название')),
                ('skills', models.CharField(max_length=150, verbose_name='Навыки')),
                ('salary_min', models.PositiveSmallIntegerField(verbose_name='Мин зарплата')),
                ('salary_max', models.PositiveSmallIntegerField(verbose_name='Макс зарплата')),
                ('published', models.DateTimeField(default=datetime.datetime(2021, 2, 23, 22, 29, 52, 902339),
                                                   verbose_name='Опубликовано')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies',
                                              to='company.Company')),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies',
                                                 to='company.Speciality')),
            ],
            options={
                'verbose_name': 'Вакансия',
                'verbose_name_plural': 'Вакансии',
            },
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Имя')),
                ('surname', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('status', models.CharField(
                    choices=[('NS', 'Не ищу работу'), ('SS', 'Рассматриваю предложения'), ('IS', 'Ищу работу')],
                    default='NS', max_length=40, verbose_name='Статус')),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Вознаграждение')),
                ('grade', models.CharField(
                    choices=[('TR', 'Стажер'), ('JR', 'Джуноир'), ('MD', 'Мидл'), ('SR', 'Синьор'), ('TM', 'Лид')],
                    default='TR', max_length=10, verbose_name='Квалификация')),
                ('education', models.CharField(max_length=100, verbose_name='Образование')),
                ('experience', models.CharField(max_length=100, verbose_name='Опыт работы')),
                ('portfolio', models.URLField(verbose_name='Ссылка на портфолио')),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Speciality',
                                                 verbose_name='Специализация')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                              verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Резюме',
                'verbose_name_plural': 'Резюме',
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=40, verbose_name='Имя')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('letter', models.TextField(blank=True, default='', max_length=1000, verbose_name='Письмо')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                           verbose_name='Пользователь')),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Vacancy',
                                              verbose_name='Вакансия')),
            ],
            options={
                'verbose_name': 'Отклик',
                'verbose_name_plural': 'Отклики',
            },
        ),
    ]