from django.db import models


class Sponsor(models.Model):
    name = models.CharField(max_length=64)
    logo = models.ImageField(upload_to='sponsors')
    website = models.URLField()
    category = models.CharField(max_length=64)
