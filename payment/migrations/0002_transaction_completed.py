# Generated by Django 3.0.3 on 2020-02-16 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
