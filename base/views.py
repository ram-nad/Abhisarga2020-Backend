from django.shortcuts import render


def home(request):
    return render(request, 'base/home.html')


def contact(request):
    return render(request, 'home/contact.html')
