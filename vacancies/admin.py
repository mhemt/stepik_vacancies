from django.contrib import admin

from .models import Company, Specialty, Skill, Vacancy, Application, Resume


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'owner',
        'location',
        'logo',
        'description',
        'employee_count',
    )
    list_filter = ('owner',)
    search_fields = ('name',)


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'title', 'picture')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'specialty',
        'company',
        'description',
        'salary_min',
        'salary_max',
        'published_at',
    )
    list_filter = ('specialty', 'company', 'published_at')
    raw_id_fields = ('skills',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'written_username',
        'written_phone',
        'written_cover_letter',
        'vacancy',
        'user',
    )
    list_filter = ('vacancy', 'user')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'name',
        'surname',
        'status',
        'salary',
        'specialty',
        'grade',
        'education',
        'experience',
        'portfolio',
    )
    list_filter = ('owner', 'specialty')
    search_fields = ('name',)
