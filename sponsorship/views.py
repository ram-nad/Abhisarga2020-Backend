from django.shortcuts import render
from .models import Sponsor


def sponsors_view(request):
    s = Sponsor.objects.all().order_by('category__priority')
    return render(request, 'sponsorship/sponsors.html', context={'sponsors': s})
