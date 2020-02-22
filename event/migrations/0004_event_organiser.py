# Generated by Django 3.0.3 on 2020-02-22 09:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0003_auto_20200222_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='organiser',
            field=models.ForeignKey(default=None, limit_choices_to={'is_administrator': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organised_events', to=settings.AUTH_USER_MODEL),
        ),
    ]