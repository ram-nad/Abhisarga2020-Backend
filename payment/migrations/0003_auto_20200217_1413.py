# Generated by Django 3.0.3 on 2020-02-17 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_transaction_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='completed',
        ),
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('N', 'New'), ('P', 'Pending'), ('F', 'Failed'), ('S', 'Success')], default='N', max_length=1),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]