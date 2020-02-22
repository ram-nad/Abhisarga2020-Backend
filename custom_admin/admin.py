from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy

from event.models import Event
from registration.models import User


class AdministratorAuthForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if user.is_staff or user.is_administrator:
            pass
        else:
            raise ValidationError()


class CustomAdminSite(AdminSite):
    site_title = gettext_lazy('Admin | Abhisarga 2020')

    index_title = 'Dashboard'

    site_header = gettext_lazy('Abhisarga Dashboard')

    def has_permission(self, request):
        if request.user.is_anonymous:
            return False
        else:
            return request.user.is_active and (request.user.is_staff or request.user.is_administrator)


custom_admin_site = CustomAdminSite(name='custom_admin')


class CustomUserAdmin(ModelAdmin):
    fields = ('email', 'password')

    def has_view_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_staff=False, is_superuser=False, is_administrator=True)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return True

    def save_model(self, request, obj, form, change):
        password = obj.password
        obj.set_password(password)
        obj.is_administrator = True
        obj.is_active = True
        super().save_model(request, obj, form, change)


custom_admin_site.register(User, CustomUserAdmin)


class EventOrganiserSite(AdminSite):
    site_title = gettext_lazy('Event Organisers | Abhisarga 2020')

    index_title = 'Dashboard'

    site_header = gettext_lazy('Abhisarga Dashboard')

    login_form = AdministratorAuthForm

    def has_permission(self, request):
        if request.user.is_anonymous:
            return False
        else:
            return request.user.is_staff or request.user.is_administrator


event_admin_site = EventOrganiserSite(name='event_organiser')


class CustomEventAdmin(ModelAdmin):
    fields = (
        'name', 'category', 'description', 'vne', 'dt', 'rls', 'poster', 'contact_number', 'short_description', 'f_p',
        's_p', 't_p')

    def has_view_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_staff:
            return True
        if not isinstance(obj, Event):
            return False
        return request.user == obj.organiser

    def has_add_permission(self, request):
        return False

    def has_module_permission(self, request):
        return True


event_admin_site.register(Event, CustomEventAdmin)
