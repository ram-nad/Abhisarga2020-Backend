from django.contrib.admin import ModelAdmin, site as admin_site
from custom_admin.admin import custom_admin_site
from .models import College, EventCategory

admin_site.register(College)
admin_site.register(EventCategory)
custom_admin_site.register(College)
custom_admin_site.register(EventCategory)
