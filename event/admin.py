from django.contrib.admin import ModelAdmin

from custom_admin.admin import custom_admin_site
from .models import *


custom_admin_site.register(Event)
