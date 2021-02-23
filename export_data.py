import os
import django

from vacancies.models import Company, Skill, Specialty, Vacancy
import data

os.environ['DJANGO_SETTINGS_MODULE'] = 'stepik_vacancies.settings'
django.setup()


def import_specialities():
    for specialty in data.specialties:
        Specialty.objects.create(
            code=specialty['code'],
            title=specialty['title'],
        )


def import_companies():
    for company in data.companies:
        Company.objects.create(
            id=company['id'],
            name=company['title'],
            location=company['location'],
            logo=company['logo'],
            description=company['description'],
            employee_count=company['employee_count'],
        )


def import_skills_jobs():
    skills = set()
    for job in data.jobs:
        skills.update(set(job['skills'].split(', ')))
    for skill in skills:
        Skill.objects.create(name=skill)

    for job in data.jobs:
        vacancy = Vacancy.objects.create(
            id=job['id'],
            title=job['title'],
            company=Company.objects.get(id=job['company']),
            specialty=Specialty.objects.get(code=job['specialty']),
            description=job['description'],
            salary_min=job['salary_from'],
            salary_max=job['salary_to'],
            published_at=job['posted'],
        )
        for skill in job['skills'].split(', '):
            vacancy.skills.add(Skill.objects.get(name=skill))
            vacancy.save()


def main():
    import_specialities()
    import_companies()
    import_skills_jobs()


if __name__ == '__main__':
    main()
