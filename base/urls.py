from django.urls import path

from .views import home, contact

urlpatterns = [
    path('', home, name='home'),
    path('contact', contact, name='contact'),
    path('404', contact, name='not_found'),
]
