# Generated by Django 3.0.3 on 2020-02-21 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import registration.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0002_auto_20200216_2249'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_administrator', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=13, validators=[registration.validators.validate_phone])),
                ('profile_pic', models.ImageField(default='volunteer/default_volunteer_pic.jpg', upload_to='volunteer')),
                ('role', models.CharField(max_length=50)),
                ('facebook', models.URLField(blank=True, verbose_name='Facebook Profile')),
                ('linkedin', models.URLField(blank=True, verbose_name='LinkedIn Profile')),
                ('instagram', models.URLField(blank=True, verbose_name='Instagram Profile')),
                ('twitter', models.URLField(blank=True, verbose_name='Twitter Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('phone_number', models.CharField(blank=True, max_length=13, unique=True, validators=[registration.validators.validate_phone])),
                ('profile_pic', models.ImageField(default='profilepics/default_profile_pic.jpg', upload_to='profilepics')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('college', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='base.College')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
