# Generated by Django 3.0.3 on 2020-02-25 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_registration', '0003_auto_20200225_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventregistration',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Last Updated'),
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='registration_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Registration Time'),
        ),
    ]
