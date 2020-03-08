from django.db import models
from django.utils.html import escape
from django.utils.safestring import SafeString

from event.models import Event
from registration.models import Profile


class EventRegistration(models.Model):
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='registrations',
                             verbose_name="Participant")
    members = models.TextField(max_length=2000, verbose_name="Team Members", blank=True)
    extra_param_1_value = models.CharField(max_length=160, blank=True, verbose_name="Parameter 1")
    extra_param_2_value = models.CharField(max_length=160, blank=True, verbose_name="Parameter 2")
    extra_param_3_value = models.CharField(max_length=160, blank=True, verbose_name="Parameter 3")
    registration_time = models.DateTimeField(auto_now_add=True, verbose_name="Registration Time")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"
        unique_together = ('event', 'user')

    @property
    def is_team_event(self):
        return self.event.team_event

    @property
    def participant(self):
        return self.user.name

    @property
    def list_extra_params(self):
        result = ()
        if self.event.extra_param_1_name != '':
            result = result + ('first_param',)
        if self.event.extra_param_2_name != '':
            result = result + ('second_param',)
        if self.event.extra_param_3_name != '':
            result = result + ('third_param',)
        return result

    @property
    def first_param(self):
        if self.event.extra_param_1_name != '':
            return SafeString("<strong>" + escape(self.event.extra_param_1_name) + "</strong>: ") + escape(
                self.extra_param_1_value)

    @property
    def second_param(self):
        if self.event.extra_param_2_name != '':
            return SafeString("<strong>" + escape(self.event.extra_param_2_name) + "</strong>: ") + escape(
                self.extra_param_2_value)

    @property
    def third_param(self):
        if self.event.extra_param_3_name != '':
            return SafeString("<strong>" + escape(self.event.extra_param_3_name) + "</strong>: ") + escape(
                self.extra_param_3_value)

    @property
    def name(self):
        return self.event.name

    @property
    def category(self):
        return self.event.category.name

    @property
    def email(self):
        return self.user.email

    @property
    def college(self):
        return self.user.college.name

    @property
    def team_leader(self):
        return self.user.name

    @property
    def team_members(self):
        return self.participant + "\n" + self.members

    @property
    def member_list(self):
        return filter(lambda x: len(x) > 0, self.members.split("\n"))

    def __str__(self):
        return self.user.email + "(" + self.name + ")"

    @property
    def get_extra_params(self):
        return [f for f in
                [(self.event.extra_param_1_name, self.event.extra_param_1_optional, self.extra_param_1_value),
                 (self.event.extra_param_2_name, self.event.extra_param_2_optional, self.extra_param_2_value),
                 (self.event.extra_param_3_name, self.event.extra_param_3_optional, self.extra_param_3_value)] if f[0]]
