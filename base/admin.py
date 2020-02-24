from django.contrib.admin import ModelAdmin
from django.contrib.admin import site as admin_site
from django.urls import reverse
from django.utils.safestring import SafeString

from custom_admin.admin import custom_admin_site
from .models import College, EventCategory

admin_site.register(College)
admin_site.register(EventCategory)

custom_admin_site.register(EventCategory)


class CustomCollege(ModelAdmin):
    list_display = ('name', 'registrants_list')
    search_fields = ('name',)

    def registrants_list(self, obj):
        a = '<a href="' + reverse("custom_admin:registration_profile_changelist") + "?college__id__exact=" + str(
            obj.pk) + '">View ' + str(obj.students.count() if obj.students else 0) + ' Registrants</a>'
        return SafeString(a)


custom_admin_site.register(College, CustomCollege)
