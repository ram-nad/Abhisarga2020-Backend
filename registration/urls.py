from django.urls import path

from .views import ProfileCreateView, google_login, google_sign_in

urlpatterns = [
    path('create', ProfileCreateView.as_view(), name='signup'),
    path('gsignin', google_sign_in, name="google_sign_in"),
    path('google_login', google_login, name='google_log_in'),
]
