# Generated by Django 3.1.6 on 2021-02-23 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0008_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='portfolio',
            field=models.URLField(blank=True, default='', max_length=100),
        ),
    ]
