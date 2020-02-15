from django.shortcuts import render


def home(request):
    return render(request, 'base/home.html')


def contact(request):
    return render(request, 'home/contact.html')


def not_found(request):
    return render(request, 'base/not_found.html')
