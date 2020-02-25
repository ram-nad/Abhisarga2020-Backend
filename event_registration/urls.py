from django.urls import path

from .views import EventRegisterView, RegistrationView, RegistrationEdit, RegistrationDelete

urlpatterns = [
    path('', RegistrationView.as_view(), name='event_registration'),
    path('register', EventRegisterView.as_view(), name='event_register_view'),
    path('edit', RegistrationEdit.as_view(), name="event_registration_edit"),
    path('deregister', RegistrationDelete.as_view(), name="event_deregistration"),
]
