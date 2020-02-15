from django.urls import path

from .views import *

urlpatterns = [
    path('', sponsors_view, name='sponsors'),
]
