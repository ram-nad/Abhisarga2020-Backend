from django.shortcuts import render

from .models import Category


def sponsors_view(request):
    c = Category.objects.all().order_by('priority')
    return render(request, 'base/sponsors.html', context={'category': c})
