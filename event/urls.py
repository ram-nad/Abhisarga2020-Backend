from django.urls import path

from .views import *

urlpatterns = [
    path('', EventListView.as_view(), name='events'),
    path('<int:pk>', EventDetailView.as_view(), name="event_detail")
]
