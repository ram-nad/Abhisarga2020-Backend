from django.contrib.auth.views import auth_logout
from django.urls import path

from .views import ProfileCreateView, google_login, UserLoginView

urlpatterns = [
    path('create', ProfileCreateView.as_view(), name='signup'),
    path('google_login', google_login, name='google_log_in'),
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', auth_logout, name='logout'),
]
