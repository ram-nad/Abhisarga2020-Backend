"""AbhisargaBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = permission_denied
handler500 = internal_server_error
handler404 = not_found
handler400 = bad_request
