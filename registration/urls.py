from django.contrib.auth.views import auth_logout
from django.urls import path

from .views import UserLoginView, ProfileMakeView, profile_create_get, profile_create_post

urlpatterns = [
    path('create', ProfileMakeView.as_view(), name='signup'),
    path('new/<email>/<token>', profile_create_get, name='profile_create'),
    path('new', profile_create_post, name='profile_create_post'),
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', auth_logout, name='logout'),
]
