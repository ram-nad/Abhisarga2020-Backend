# Generated by Django 3.0.3 on 2020-02-25 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_registration', '0002_auto_20200225_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventregistration',
            name='extra_param_1_value',
            field=models.CharField(blank=True, max_length=160, verbose_name='Parameter 1'),
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='extra_param_2_value',
            field=models.CharField(blank=True, max_length=160, verbose_name='Parameter 2'),
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='extra_param_3_value',
            field=models.CharField(blank=True, max_length=160, verbose_name='Parameter 3'),
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='members',
            field=models.TextField(blank=True, max_length=2000, verbose_name='Team Members'),
        ),
    ]