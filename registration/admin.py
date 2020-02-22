from django.contrib import admin

from custom_admin.admin import custom_admin_site
from .models import *

admin.site.register(Profile)
admin.site.register(User)

custom_admin_site.register(Volunteer)
custom_admin_site.register(User)
