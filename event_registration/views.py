from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from event.models import Event
from payment.models import Transaction
from .models import EventRegistration


class EventRegisterView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            registration = EventRegistration.objects.get(event_id=pk, user=request.user.profile)
            return render(request, 'event_registration/registration_detail.html',
                          context={'registration': registration})

        except EventRegistration.DoesNotExist:
            try:
                event = Event.objects.get(pk=pk)
            except Event.DoesNotExist:
                return redirect('not_found')

            extra_fields = event.get_extra_params()
            if extra_fields:
                return render(request, 'event_registration/registration_form.html', context={'fields': extra_fields})
            else:
                return render(request, 'event_registration/registration_form.html', context={'no_extra_fields': True})

    def post(self, request, pk):
        if EventRegistration.objects.filter(event_id=pk, user=request.user.profile).count() > 0:
            registration = EventRegistration.objects.get(event_id=pk, user=request.user.profile)
            return render(request, 'event_registration/registration_detail.html',
                          context={'registration': registration})
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return redirect('not_found')
        print(request.POST)

        registration = EventRegistration()
        registration.event = event
        registration.user = request.user.profile
        transaction = Transaction.objects.create(made_by=request.user, amount=event.amount)
        transaction.save()
        registration.transaction = transaction

        if event.extra_param_1_name:
            registration.extra_param_1_value = request.POST.get(event.extra_param_1_name, '')
        if event.extra_param_2_name:
            registration.extra_param_2_value = request.POST.get(event.extra_param_2_name, '')
        if event.extra_param_3_name:
            registration.extra_param_3_value = request.POST.get(event.extra_param_3_name, '')
        registration.save()

        return render(request, 'event_registration/registration_detail.html',
                      context={'registration': registration})
