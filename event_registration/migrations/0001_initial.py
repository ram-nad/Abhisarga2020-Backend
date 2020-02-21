# Generated by Django 3.0.3 on 2020-02-16 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('event', '0001_initial'),
        ('payment', '0001_initial'),
        ('registration', '0007_remove_volunteer_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra_param_1_value', models.CharField(default='', max_length=160)),
                ('extra_param_2_value', models.CharField(default='', max_length=160)),
                ('extra_param_3_value', models.CharField(default='', max_length=160)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='event.Event')),
                ('transaction', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.Transaction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='registration.Profile')),
            ],
        ),
    ]