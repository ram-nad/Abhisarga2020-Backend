from django.db import models


class College(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return "College: " + self.name


class EventCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Event Categories"

    @property
    def slug_name(self):
        return self.name.replace(" ", "-").lower()
