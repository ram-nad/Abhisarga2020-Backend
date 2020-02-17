# Generated by Django 3.0.3 on 2020-02-17 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0008_auto_20200216_2301'),
        ('payment', '0003_auto_20200217_1413'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='status',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='transaction_id',
        ),
        migrations.AddField(
            model_name='transaction',
            name='reason',
            field=models.CharField(default='none', max_length=256),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='made_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='registration.Profile'),
        ),
    ]
