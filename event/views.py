from django.shortcuts import render, redirect
from django.views import View
from .models import Event


class EventListView(View):
    def get(self, request):
        return render(request, 'event/events.html', context={'events': Event.objects.all()})


# class EventListView(View):


class EventDetailView(View):
    def get(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return redirect('not_found')
        return render(request, 'event/event_page.html', context={'event': event})
