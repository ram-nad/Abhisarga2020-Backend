from django.urls import path

from .views import home, get_college_list

urlpatterns = [
    path('', home, name='home'),
    path('colleges', get_college_list, name="college_list"),
]
