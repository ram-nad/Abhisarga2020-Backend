from django.core.exceptions import ValidationError
from django.db import models, transaction

from base.models import EventCategory
from registration.models import User
from registration.validators import validate_phone


class Event(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(to=EventCategory, related_name="events", on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=2000)
    vne = models.CharField(max_length=300, verbose_name="Venue", blank=True, null=True)
    dt = models.DateField(verbose_name="Date", null=True, blank=True)
    rls = models.TextField(max_length=5000, verbose_name="Rules")
    poster = models.ImageField(upload_to="events", default="events/default_event_poster.jpg")
    contact_number = models.CharField(max_length=13, validators=[validate_phone])
    short_description = models.CharField(max_length=40, default="")
    f_p = models.CharField(max_length=5, verbose_name="First Prize", blank=True, null=True)
    s_p = models.CharField(max_length=5, verbose_name="Second Prize", blank=True, null=True)
    t_p = models.CharField(max_length=5, verbose_name="Third Prize", blank=True, null=True)

    organiser = models.ForeignKey(to=User, related_name="organised_events", null=True, on_delete=models.SET_NULL,
                                  limit_choices_to={'is_administrator': True}, blank=True)

    team_event = models.BooleanField(default=False)
    team_min_size = models.PositiveIntegerField(default=1)
    team_max_size = models.PositiveIntegerField(default=1)
    max_participant = models.PositiveIntegerField(default=50)
    registration_open = models.BooleanField(default=False)
    extra_param_1_name = models.CharField(max_length=40, blank=True, default="")
    extra_param_1_optional = models.BooleanField(default=False)
    extra_param_2_name = models.CharField(max_length=40, blank=True, default="")
    extra_param_2_optional = models.BooleanField(default=False)
    extra_param_3_name = models.CharField(max_length=40, blank=True, default="")
    extra_param_3_optional = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if self.team_event:
            if self.team_min_size > self.team_max_size:
                raise ValidationError("Min team size must be greater than Max team size")
        self.contact_number = validate_phone(self.contact_number)
        if not self.team_event:
            self.team_max_size = 1
            self.team_max_size = 1

    def __str__(self):
        return self.name

    @property
    def get_extra_params(self):
        return [f for f in [(self.extra_param_1_name, self.extra_param_1_optional),
                            (self.extra_param_2_name, self.extra_param_2_optional),
                            (self.extra_param_3_name, self.extra_param_3_optional)] if f[0]]

    @property
    def has_extra_params(self):
        return self.extra_param_1_name != '' or self.extra_param_2_name != '' or self.extra_param_3_name != ''

    @property
    @transaction.atomic
    def max_limit_reached(self):
        event = Event.objects.select_for_update(of=()).get(pk=self.pk)
        count = event.participants.count()
        return count == event.max_participant

    @property
    def simple_max_limit_reached(self):
        event = Event.objects.get(pk=self.pk)
        count = event.participants.count()
        return count == event.max_participant

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
        if self.vne is None or self.vne == '':
            return "-----"
        return self.vne

    @property
    def date(self):
        if self.dt is None:
            return "-----"
        return self.dt.strftime("%d %B")
