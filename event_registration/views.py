from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View

from AbhisargaBackend.settings import NEXT_PARAMETER
from base.views import bad_request, not_found
from event.models import Event
from .models import EventRegistration

already_full_message = {'title': 'Registration Full',
                        'message': "Sorry, registration for this event is already full. "
                                   "Please check for other events.",
                        'next': {'name': "Explore other events", 'url': reverse_lazy('events')}}


def helper_base(request, event, registration, error):
    if not event.extra_param_1_name == '':
        value = request.POST.get(event.extra_param_1_name, '').strip()
        if not event.extra_param_1_optional and value == '':
            error.update({event.extra_param_1_name: "This field is required"})
        else:
            registration.extra_param_1_value = value
    if not event.extra_param_2_name == '':
        value = request.POST.get(event.extra_param_2_name, '').strip()
        if not event.extra_param_2_optional and value == '':
            error.update({event.extra_param_2_name: "This field is required"})
        else:
            registration.extra_param_2_value = value
    if not event.extra_param_3_name == '':
        value = request.POST.get(event.extra_param_3_name, '').strip()
        if not event.extra_param_3_optional and value == '':
            error.update({event.extra_param_3_name: "This field is required"})
        else:
            registration.extra_param_3_value = value
    if event.team_event:
        value = request.POST.getlist('members', None)
        if (value is None or len(value) == 0) and event.team_min_size > 1 or len(value) < (event.team_min_size - 1):
            error.update({'members': "Minimum " + str(event.team_min_size) + " members are required in team"})
        elif len(value) > (event.team_max_size - 1):
            error.update({'members': "Maximum " + str(event.team_min_size) + " members are allowed in team"})
        elif True in list(map(lambda x: x.strip() == '', value)):
            error.update({'members': "Values of this field cannot be empty."})
        else:
            registration.members = "\n".join(value)
    try:
        registration.full_clean()
    except ValidationError as E:
        error.update(E.message_dict)


class EventRegisterView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = NEXT_PARAMETER

    def get(self, request, pk):
        try:
            registration = EventRegistration.objects.get(event_id=pk, user=request.user.profile)
            salutation = "You are"
            if registration.is_team_event:
                salutation = "Your Team is"
            message = {'title': 'Already Registered',
                       'message': salutation + " already registered for this event.",
                       'next': {'name': "Explore other events", 'url': reverse('events')}}
            return render(request, 'base/message.html', context=message)

        except EventRegistration.DoesNotExist:
            try:
                event = Event.objects.get(pk=pk)
            except Event.DoesNotExist:
                return not_found(request)

            if event.simple_max_limit_reached:
                return render(request, 'base/message.html', context=already_full_message)

            return render(request, 'event_registration/registration.html', context={'event': event})

    @transaction.atomic
    def post(self, request, pk):
        if EventRegistration.objects.filter(event_id=pk, user=request.user.profile).count() > 0:
            return bad_request(request)

        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return not_found(request)

        if event.max_limit_reached:
            return render(request, 'base/message.html', context=already_full_message)

        registration = EventRegistration()
        registration.event = event
        registration.user = request.user.profile

        error = dict()

        helper_base(request, event, registration, error)

        if error:
            return render(request, 'event_registration/registration.html',
                          context={'event': event, 'error': error})
        else:
            registration.save()

        salutation = "You have"
        if registration.is_team_event:
            salutation = "Your Team has"
        message = {'title': 'Registration Successful',
                   'message': salutation + " successfully registered for " + event.name + " at Abhisarga 2020.",
                   'next': {'name': "Explore other events", 'url': reverse('events')}}
        return render(request, 'base/message.html', context=message)


class RegistrationView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = NEXT_PARAMETER

    def get(self, request, pk):
        try:
            registration = EventRegistration.objects.get(event_id=pk, user=request.user.profile)
            return render(request, 'event_registration/registration.html',
                          context={'view': True, 'registration': registration, 'event': registration.event})
        except EventRegistration.DoesNotExist:
            return not_found(request)


class RegistrationEdit(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = NEXT_PARAMETER

    def get(self, request, pk):
        try:
            registration = EventRegistration.objects.get(event_id=pk, user=request.user.profile)
            return render(request, 'event_registration/registration.html',
                          context={'view': False, 'registration': registration, 'event': registration.event})
        except EventRegistration.DoesNotExist:
            return not_found(request)

    def post(self, request, pk):
        try:
            registration = EventRegistration.objects.get(event_id=pk, user=request.user.profile)
            event = Event.objects.get(pk=pk)

            error = dict()
            helper_base(request, event, registration, error)

            if error:
                extra_fields = event.get_extra_params()
                return render(request, 'event_registration/registration.html',
                              context={'view': False, 'registration': registration, 'error': error})
            else:
                registration.save()

            return render(request, 'event_registration/registration.html',
                          context={'view': True, 'registration': registration, 'event': registration.event})
        except (EventRegistration.DoesNotExist, Event.DoesNotExist):
            return not_found(request)


class RegistrationDelete(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = NEXT_PARAMETER

    def get(self, request, pk):
        try:
            registration = EventRegistration.objects.get(event_id=pk, user=request.user.profile)
            event = Event.objects.get(pk=pk)
            registration.delete()
            salutation = "You have"
            if registration.is_team_event:
                salutation = "Your Team has"
            message = {'title': 'De-Registration Successful',
                       'message': salutation + " been successfully de-registered from " + event.name + " at Abhisarga "
                                                                                                       "2020.",
                       'next': {'name': "Explore other events", 'url': reverse('events')}}
            return render(request, 'base/message.html', context=message)
        except (EventRegistration.DoesNotExist, Event.DoesNotExist):
            return not_found(request)
