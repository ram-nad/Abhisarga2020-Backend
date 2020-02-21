# Generated by Django 3.0.3 on 2020-02-20 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0009_auto_20200217_1918'),
    ]

    operations = [
        migrations.RenameField(
            model_name='volunteer',
            old_name='fb',
            new_name='facebook',
        ),
        migrations.RenameField(
            model_name='volunteer',
            old_name='insta',
            new_name='instagram',
        ),
        migrations.AddField(
            model_name='volunteer',
            name='twitter',
            field=models.URLField(blank=True, verbose_name='Twitter Profile'),
        ),
    ]