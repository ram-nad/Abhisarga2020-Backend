from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.utils.translation import gettext as _, gettext_lazy


class CustomAdminSite(AdminSite):
    site_title = gettext_lazy('Admin Panel')

    # Text to put in each page's <h1>.
    site_header = gettext_lazy('Admin Panel')

    # Text to put at the top of the admin index page.
    index_title = gettext_lazy('Admin Panel')


custom_admin_site = CustomAdminSite(name='custom_admin')
