from django.urls import path
from .views import *

urlpatterns = [
    path('<slug:order_id>/pay', initiate_payment, name='paytm_initiate_payment'),
    path('callback', callback, name='callback'),
]
