from django.db import models

from base.models import EventCategory
from registration.models import Volunteer


class Event(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(to=EventCategory, related_name="events", on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=500)
    team_event = models.BooleanField(default=False)
    max_participant = models.PositiveIntegerField()
    team_min_size = models.PositiveIntegerField(default=1)
    team_max_size = models.PositiveIntegerField(default=1)
    venue = models.CharField(max_length=300)
    time = models.TimeField()
    date = models.DateField()
    registration_open = models.BooleanField(default=True)
    organiser = models.ForeignKey(to=Volunteer, related_name="organised_events", null=True, on_delete=models.SET_NULL)
    co_organiser = models.ForeignKey(to=Volunteer, related_name="co_organised_events", null=True, blank=True,
                                     on_delete=models.SET_NULL)
    prizes = models.TextField(max_length=300)
    rules = models.TextField(max_length=1000)
    extra_param_1_name = models.CharField(max_length=40, default="")
    extra_param_2_name = models.CharField(max_length=40, default="")
    extra_param_3_name = models.CharField(max_length=40, default="")

    def __str__(self):
        return self.name

    def get_extra_params(self):
        return [f for f in [self.extra_param_1_name, self.extra_param_2_name, self.extra_param_3_name] if f]
