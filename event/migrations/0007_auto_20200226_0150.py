# Generated by Django 3.0.3 on 2020-02-25 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_auto_20200225_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='extra_param_1_optional',
            field=models.BooleanField(default=False, verbose_name='Extra parameter 1 is optional'),
        ),
        migrations.AlterField(
            model_name='event',
            name='extra_param_2_optional',
            field=models.BooleanField(default=False, verbose_name='Extra parameter 1 is optional'),
        ),
        migrations.AlterField(
            model_name='event',
            name='extra_param_3_optional',
            field=models.BooleanField(default=False, verbose_name='Extra parameter 1 is optional'),
        ),
    ]