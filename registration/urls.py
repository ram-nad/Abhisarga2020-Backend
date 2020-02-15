from django.urls import path
from .views import *

urlpatterns = [
    path('create', ProfileCreateView.as_view(), name='signup')
]
