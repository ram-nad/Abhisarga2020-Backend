from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from .models import EventRegistration


# class EventRegistrationDetailView(LoginRequiredMixin, View):
#     def post(self, request, pk):
#

