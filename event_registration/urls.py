from django.urls import path
from .views import EventRegisterView

urlpatterns = [
    path('register', EventRegisterView.as_view(), name='event_register_view'),
]
