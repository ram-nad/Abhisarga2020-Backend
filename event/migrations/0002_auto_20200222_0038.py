# Generated by Django 3.0.3 on 2020-02-21 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='dt',
            field=models.DateField(null=True, verbose_name='Date'),
        ),
    ]
