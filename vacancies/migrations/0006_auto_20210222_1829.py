# Generated by Django 3.1.6 on 2021-02-22 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0005_auto_20210222_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='salary_max',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='salary_min',
            field=models.IntegerField(default=0),
        ),
    ]
