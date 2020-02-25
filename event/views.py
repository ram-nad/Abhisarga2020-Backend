from django.shortcuts import render
from django.views import View

from base.models import EventCategory
from base.views import not_found
from .models import Event


class EventListView(View):
    def get(self, request):
        return render(request, 'event/events.html', context={'categories': EventCategory.objects.all()})


class EventDetailView(View):
    def get(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return not_found(request)
        return render(request, 'event/event.html', context={'event': event})
