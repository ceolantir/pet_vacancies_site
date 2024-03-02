from django.contrib import admin

from .models import Vacancy, Company, Speciality, Application, Resume


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'speciality',
        'company',
        'skills',
        'salary_min',
        'salary_max',
        'published',
    )
    list_filter = ('speciality', 'company', 'published')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'location',
        'logo',
        'description',
        'employee_count',
        'owner',
    )
    list_display_links = ('title',)
    list_filter = ('owner',)


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'title', 'image')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone', 'letter', 'vacancy', 'user')
    list_filter = ('vacancy', 'user')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'name',
        'surname',
        'status',
        'salary',
        'speciality',
        'grade',
        'education',
        'experience',
        'portfolio',
    )
    list_filter = ('user', 'speciality')
    search_fields = ('name',)
