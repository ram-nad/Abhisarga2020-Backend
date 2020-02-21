from django.db import models

from base.models import EventCategory
from registration.models import Volunteer
from registration.validators import validate_phone


class Event(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(to=EventCategory, related_name="events", on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=500)
    vne = models.CharField(max_length=300, verbose_name="Venue", blank=True, null=True)
    dt = models.DateField(verbose_name="Date", null=True, blank=True)
    rls = models.TextField(max_length=1000, verbose_name="Rules")
    poster = models.ImageField(upload_to="events", default="events/default_event_poster.jpg")
    contact_number = models.CharField(max_length=13, validators=[validate_phone])
    short_description = models.CharField(max_length=20, default="")
    f_p = models.CharField(max_length=5, verbose_name="First Prize", blank=True, null=True)
    s_p = models.CharField(max_length=5, verbose_name="Second Prize", blank=True, null=True)
    t_p = models.CharField(max_length=5, verbose_name="Third Prize", blank=True, null=True)

    # organiser = models.ForeignKey(to=Volunteer, related_name="organised_events", null=True, on_delete=models.SET_NULL)
    #
    # team_event = models.BooleanField(default=False)
    # max_participant = models.PositiveIntegerField()
    # team_min_size = models.PositiveIntegerField(default=1)
    # team_max_size = models.PositiveIntegerField(default=1)
    # registration_open = models.BooleanField(default=True)
    # amount = models.IntegerField(default=0)
    # extra_param_1_name = models.CharField(max_length=40, blank=True, default="")
    # extra_param_2_name = models.CharField(max_length=40, blank=True, default="")
    # extra_param_3_name = models.CharField(max_length=40, blank=True, default="")

    def clean(self):
        super().clean()
        self.contact_number = validate_phone(self.contact_number)

    def __str__(self):
        return self.name

    # def get_extra_params(self):
    #     return [f for f in [self.extra_param_1_name, self.extra_param_2_name, self.extra_param_3_name] if f]

    @property
    def first_prize(self):
        if self.f_p is None:
            return "---"
        try:
            a = int(self.f_p)
            return "₹ {:,d}".format(a)
        except ValueError:
            return "₹"

    @property
    def second_prize(self):
        if self.s_p is None:
            return "---"
        try:
            a = int(self.s_p)
            return "₹ {:,d}".format(a)
        except ValueError:
            return "₹"

    @property
    def third_prize(self):
        if self.t_p is None:
            return "---"
        try:
            a = int(self.t_p)
            return "₹ {:,d}".format(a)
        except ValueError:
            return "₹"

    @property
    def rules(self):
        return list(map(str.strip, filter(lambda x: len(x) > 0, self.rls.split("\n"))))

    @property
    def venue(self):
        if self.vne in [None, '']:
            return "-----"
        return self.vne

    @property
    def date(self):
        if self.dt is None:
            return "-----"
        return self.dt.strftime("%d %B")
