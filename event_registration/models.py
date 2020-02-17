from django.db import models


class EventRegistration(models.Model):
    event = models.ForeignKey(to='event.Event', on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(to='registration.Profile', on_delete=models.CASCADE, related_name='registrations')
    extra_param_1_value = models.CharField(max_length=160, default="")
    extra_param_2_value = models.CharField(max_length=160, default="")
    extra_param_3_value = models.CharField(max_length=160, default="")
    transaction = models.OneToOneField(to='payment.Transaction', null=True, blank=True, on_delete=models.SET_NULL)

