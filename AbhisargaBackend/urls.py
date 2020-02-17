from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from base.views import permission_denied, internal_server_error, not_found, bad_request
from custom_admin.admin import custom_admin_site

urlpatterns = [
  path('', include('base.urls')),
  path('admin/', admin.site.urls),
  path('staff/', custom_admin_site.urls),
  path('sponsors/', include('sponsorship.urls')),
  path('profile/', include('registration.urls')),
  path('event/<int:pk>/', include('event_registration.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = permission_denied
handler500 = internal_server_error
handler404 = not_found
handler400 = bad_request
