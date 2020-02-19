from django.urls import path

from .views import *

urlpatterns = [
    path('create', ProfileMakeView.as_view(), name='signup'),
    path('new/<b64id>/<token>', profile_create_get, name='profile_create'),
    path('new', profile_create_post, name='profile_create_post'),
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('change_password', PasswordChangeView.as_view(), name="password_change"),
    path('change_password_done', PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('reset_password', PasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<idb64>/<token>', PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
