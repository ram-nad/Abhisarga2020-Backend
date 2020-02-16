from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from event.models import Event
from .models import EventRegistration


class EventRegisterView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            registration = EventRegistration.objects.get(event_id=pk, user=request.user)
            return render(request, 'event_registration/registration_detail.html',
                          context={'registration': registration})

        except EventRegistration.DoesNotExist:
            try:
                event = Event.objects.get(pk=pk)
            except Event.DoesNotExist:
                return redirect('not_found')

            extra_fields = event.get_extra_params()
            if extra_fields:
                return render(request, 'event_registration/registration_form.html', context={'no_extra_fields': True})
            else:
                return render(request, 'event_registration/registration_form.html', context={'fields': extra_fields})

    def post(self, request, pk):
        pass
