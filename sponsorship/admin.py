from django.contrib.admin import ModelAdmin
from .models import Sponsor, Category
from custom_admin.admin import custom_admin_site


class CategoryAdmin(ModelAdmin):
    model = Category


class SponsorAdmin(ModelAdmin):
    model = Sponsor


custom_admin_site.register(Category, CategoryAdmin)
custom_admin_site.register(Sponsor, SponsorAdmin)

