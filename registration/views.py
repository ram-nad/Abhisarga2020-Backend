from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.views import View

from .forms import *


class ProfileCreateView(View):
    def get(self, request):
        return render(request, 'registration/signup.html', context={'form': ProfileForm().as_p()})

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES)
        try:
            form.save()
            return redirect('home')
        except ValidationError as E:
            return render(request, 'registration/signup.html',
                          context={'form': ProfileForm().as_p(), 'errors': E.message_dict})
        except ValueError:
            return render(request, 'registration/signup.html',
                          context={'form': ProfileForm(request.POST).as_p(), 'errors': form.errors})


class UserLoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html', context={'form': LoginForm().as_p()})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email, password = data['email'], data['password']
            u = authenticate(request, email=email, password=password)
            if u is None:
                return render(request, 'registration/login.html',
                              context={'form': LoginForm().as_p(), 'error': 'Wrong Email or Password'})
            auth_login(request, u)
            # TODO : redirect to profile or next
            return redirect('home')
        return render(request, 'registration/login.html',
                      context={'form': LoginForm().as_p(), 'error': form.errors})

