from django.contrib.admin import site as admin_site

from .models import Event

admin_site.register(Event)
