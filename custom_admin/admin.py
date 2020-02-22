from django.contrib.admin.sites import AdminSite
from django.utils.translation import gettext_lazy


class CustomAdminSite(AdminSite):
    site_title = gettext_lazy('Admin | Abhisarga 2020')

    index_title = gettext_lazy('Admin | Abhisarga 2020')

    site_header = gettext_lazy('Abhisarga Dashboard')

    def has_permission(self, request):
        if request.user.is_anonymous:
            return False
        else:
            return request.user.is_active and (request.user.is_staff or request.user.is_administrator)


custom_admin_site = CustomAdminSite(name='custom_admin')
