# Generated by Django 3.0.3 on 2020-02-25 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventregistration',
            name='members',
            field=models.TextField(default='', max_length=2000, verbose_name='Team Members'),
        ),
    ]
