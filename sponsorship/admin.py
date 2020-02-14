from django.contrib.admin import ModelAdmin
from .models import Sponsor
from custom_admin.admin import custom_admin_site


class SponsorAdmin(ModelAdmin):
    model = Sponsor


custom_admin_site.register(Sponsor, SponsorAdmin)

