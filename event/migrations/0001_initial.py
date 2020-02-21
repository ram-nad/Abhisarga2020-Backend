# Generated by Django 3.0.3 on 2020-02-21 19:28

from django.db import migrations, models
import django.db.models.deletion
import registration.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=500)),
                ('vne', models.CharField(blank=True, max_length=300, null=True, verbose_name='Venue')),
                ('dt', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('rls', models.TextField(max_length=1000, verbose_name='Rules')),
                ('poster', models.ImageField(default='events/default_event_poster.jpg', upload_to='events')),
                ('contact_number', models.CharField(max_length=13, validators=[registration.validators.validate_phone])),
                ('short_description', models.CharField(default='', max_length=20)),
                ('f_p', models.CharField(blank=True, max_length=5, null=True, verbose_name='First Prize')),
                ('s_p', models.CharField(blank=True, max_length=5, null=True, verbose_name='Second Prize')),
                ('t_p', models.CharField(blank=True, max_length=5, null=True, verbose_name='Third Prize')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='base.EventCategory')),
            ],
        ),
    ]
