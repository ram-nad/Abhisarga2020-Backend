from django import template

from event.models import Event
from event_registration.models import EventRegistration
from registration.models import User

register = template.Library()


@register.filter(name='is_registered')
def is_registered(value, event):
    if not isinstance(value, User):
        return False
    elif not hasattr(value, 'profile'):
        return False
    elif not isinstance(event, Event):
        return False
    else:
        return EventRegistration.objects.filter(event_id=event.pk, user=value.profile).count() > 0


@register.filter(name='is_registered_any')
def is_registered_any(value):
    if not isinstance(value, User):
        return False
    elif not hasattr(value, 'profile'):
        return False
    else:
        return EventRegistration.objects.filter(user=value.profile).count() > 0
