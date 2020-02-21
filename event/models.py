from django.db import models

from base.models import EventCategory
from registration.models import Volunteer
from registration.validators import validate_phone


class Event(models.Model):
    name = models.CharField(max_length=200)
    amount = models.IntegerField(default=0)
    category = models.ForeignKey(to=EventCategory, related_name="events", on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=500)
    venue = models.CharField(max_length=300)
    date = models.DateField()
    rls = models.TextField(max_length=1000, verbose_name="Rules")
    poster = models.ImageField(upload_to="events")
    contact_number = models.CharField(max_length=13, validators=[validate_phone])
    short_description = models.CharField(max_length=20)
    f_p = models.CharField(max_length=5, verbose_name="First Prize")
    s_p = models.CharField(max_length=5, verbose_name="First Prize")
    t_p = models.CharField(max_length=5, verbose_name="First Prize")

    # organiser = models.ForeignKey(to=Volunteer, related_name="organised_events", null=True, on_delete=models.SET_NULL)
    #
    # team_event = models.BooleanField(default=False)
    # max_participant = models.PositiveIntegerField()
    # team_min_size = models.PositiveIntegerField(default=1)
    # team_max_size = models.PositiveIntegerField(default=1)
    # registration_open = models.BooleanField(default=True)
    # extra_param_1_name = models.CharField(max_length=40, blank=True, default="")
    # extra_param_2_name = models.CharField(max_length=40, blank=True, default="")
    # extra_param_3_name = models.CharField(max_length=40, blank=True, default="")

    def clean(self):
        super().clean()
        self.contact_number = validate_phone(self.contact_number)

    def __str__(self):
        return self.name

    def get_extra_params(self):
        return [f for f in [self.extra_param_1_name, self.extra_param_2_name, self.extra_param_3_name] if f]

    @property
    def first_prize(self):
        a = int(self.f_p)
        return f"₹ {a:,d}"

    @property
    def second_prize(self):
        a = int(self.s_p)
        return f"₹ {a:,d}"

    @property
    def third_prize(self):
        a = int(self.t_p)
        return f"₹ {a:,d}"

    @property
    def rules(self):
        return list(map(str.strip, filter(lambda x: len(x) > 0, self.rls.split("\n"))))
