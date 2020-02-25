from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.safestring import SafeString

from event.models import Event
from registration.models import User, Profile


class AdministratorAuthForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if user.is_staff or user.is_administrator:
            pass
        else:
            raise ValidationError()


class CustomAdminSite(AdminSite):
    site_title = 'Admin | Abhisarga 2020'

    index_title = 'Dashboard'

    site_header = 'Abhisarga Dashboard'

    def has_permission(self, request):
        if request.user.is_anonymous:
            return False
        else:
            return request.user.is_active and request.user.is_staff


custom_admin_site = CustomAdminSite(name='custom_admin')


class CustomEventAdmin(ModelAdmin):
    list_display = ('name', 'category', 'organiser', 'participants_list', 'is_team_event')

    def is_team_event(self, obj):
        if obj is None:
            return False
        else:
            return obj.team_event

    is_team_event.boolean = True

    def participants_list(self, obj):
        a = '<a href="' + reverse(
            "custom_admin:event_registration_eventregistration_changelist") + "?event__exact=" + str(
            obj.pk) + '">View Participants</a>'
        return SafeString(a)


custom_admin_site.register(Event, CustomEventAdmin)


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
        user = User.objects.get_or_none(email=obj.email)
        if user is None:
            password = obj.password
            obj.set_password(password)
            obj.is_administrator = True
            obj.save()
        else:
            user.is_administrator = True
            user.save()


custom_admin_site.register(User, CustomUserAdmin)


class CustomProfileAdmin(ModelAdmin):
    fields = ('email', 'first_name', 'last_name', 'college_name', 'phone_number', 'gender', 'event_list_display')
    readonly_fields = ('email', 'name', 'college_name', 'phone_number', 'gender')

    def college_name(self, obj):
        return obj.college.name

    def has_view_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    list_display = ('email', 'name', 'college_name', 'phone_number', 'events_list')
    list_display_links = ('email',)
    list_filter = ('gender',)
    search_fields = ('user__email', 'first_name', 'last_name', 'phone_number', 'college__name')
    list_per_page = 20

    def events_list(self, obj):
        a = '<a href="' + reverse(
            "custom_admin:event_registration_eventregistration_changelist") + "?user__exact=" + str(
            obj.pk) + '">View Registered Events</a>'
        return SafeString(a)

    def event_list_display(self, obj):
        return "\n".join(map(lambda x: x.name, obj.registrations.all()))


custom_admin_site.register(Profile, CustomProfileAdmin)


class EventOrganiserSite(AdminSite):
    site_title = 'Event Organisers | Abhisarga 2020'

    index_title = 'Dashboard'

    site_header = 'Abhisarga Dashboard'

    login_form = AdministratorAuthForm

    def has_permission(self, request):
        if request.user.is_anonymous:
            return False
        else:
            return request.user.is_staff or request.user.is_administrator


event_admin_site = EventOrganiserSite(name='event_organiser')


class CustomEventAdmin(ModelAdmin):
    list_display = ('name', 'category', 'organiser', 'participants_list')
    readonly_fields = ('organiser',)

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

    def participants_list(self, obj):
        a = '<a href="' + reverse(
            "event_organiser:event_registration_eventregistration_changelist") + "?event__exact=" + str(
            obj.pk) + '">View Participants</a>'
        return SafeString(a)


event_admin_site.register(Event, CustomEventAdmin)
