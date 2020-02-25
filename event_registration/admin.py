from django.contrib.admin import ModelAdmin
from django.utils import timezone

from custom_admin.admin import custom_admin_site, event_admin_site
from .models import EventRegistration


class CustomEventReg(ModelAdmin):
    list_display = ('email', 'name', 'category', 'participant', 'reg_time')
    search_fields = ('event__name', 'user__email', 'user__first_name', 'user__last_name')

    fields = ('name', 'email', 'reg_time', 'last_update')
    readonly_fields = ('name', 'email')

    ordering = ('registration_time',)
    list_filter = ('event__name', 'event__category')

    def has_add_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def reg_time(self, obj):
        return timezone.localtime(obj.registration_time).strftime("%H:%M:%S, %d %B")

    def last_update(self, obj):
        return timezone.localtime(obj.last_updated).strftime("%H:%M:%S, %d %B")

    def get_fields(self, request, obj=None):
        if obj is None or not obj.is_team_event:
            return self.fields + ('participant',)
        else:
            return self.fields + ('team_leader', 'team_members')


custom_admin_site.register(EventRegistration, CustomEventReg)


class CustomEventRegOrganiser(ModelAdmin):
    list_display = ('email', 'name', 'reg_time')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')

    fields = ('name', 'email', 'reg_time', 'last_update')
    readonly_fields = ('name', 'email')

    ordering = ('registration_time',)

    list_filter = ('event__name',)

    def has_add_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        if obj is None or request.user.is_staff:
            return True
        else:
            return obj.event.organiser == request.user

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_staff:
            return False
        else:
            return obj is not None and obj.event.organiser == request.user

    def reg_time(self, obj):
        return timezone.localtime(obj.registration_time).strftime("%H:%M:%S, %d %B")

    def last_update(self, obj):
        return timezone.localtime(obj.last_updated).strftime("%H:%M:%S, %d %B")

    def get_queryset(self, request):
        if request.user.is_staff:
            return super().get_queryset(request)
        else:
            qs = super().get_queryset(request)
            print(qs)
            return qs.filter(event__organiser__pk=request.user.pk)

    def has_module_permission(self, request):
        return True

    def get_fields(self, request, obj=None):
        if obj is None or not obj.is_team_event:
            data = self.fields + ('participant',)
        else:
            data = self.fields + ('team_leader', 'team_members')
        if obj is None or request.user.is_staff:
            return data
        else:
            return data + obj.list_extra_params


event_admin_site.register(EventRegistration, CustomEventRegOrganiser)
