from django.db import models


class College(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField(blank=True)

    def __str__(self):
        return "College: " + self.name

    def has_contact(self):
        return self.contact_email == ""


class EventCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return "Event Category: " + self.name

    class Meta:
        verbose_name_plural = "Event Categories"
