from django.contrib.auth.views import auth_logout
from django.urls import path
from .views import *

urlpatterns = [
    path('create', ProfileCreateView.as_view(), name='signup'),
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', auth_logout, name='logout'),
]
