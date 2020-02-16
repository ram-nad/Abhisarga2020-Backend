from django.contrib.auth import authenticate, login as auth_login
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from AbhisargaBackend.settings import GOOGLE_CLIEND_ID, NEXT_PARAMETER
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
                          context={'form': ProfileForm(request.POST).as_p(), 'errors': E.message_dict})
        except ValueError:
            return render(request, 'registration/signup.html',
                          context={'form': ProfileForm(request.POST).as_p(), 'errors': form.errors})


class UserLoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html', context={'google_client_id': GOOGLE_CLIEND_ID})

    def post(self, request):
        if 'google-id-token' in request.POST:
            try:
                token = request.POST['google-id-token']
                user = id_token.verify_token(token, google_requests.Request(), GOOGLE_CLIEND_ID)
                if user['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                    raise ValueError('Wrong issuer.')
                u = User.objects.get(email=user['email'])
                if u is None:
                    return render(request, 'registration/login.html',
                                  context={'error': 'User does not exist', 'google_client_id': GOOGLE_CLIEND_ID})
                else:
                    auth_login(request, u)
                    if NEXT_PARAMETER in request.GET:
                        return redirect(request.GET[NEXT_PARAMETER])
                    else:
                        return redirect('home')
            except ValueError:
                return render(request, 'registration/login.html',
                              context={'error': 'Invalid Login Attempt', 'google_client_id': GOOGLE_CLIEND_ID})
        else:
            form = LoginForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                email, password = data['email'], data['password']
                u = authenticate(request, email=email, password=password)
                if u is None:
                    return render(request, 'registration/login.html',
                                  context={'error': 'Wrong Email or Password', 'google_client_id': GOOGLE_CLIEND_ID})
                auth_login(request, u)
                if NEXT_PARAMETER in request.GET:
                    return redirect(request.GET[NEXT_PARAMETER])
                else:
                    return redirect('home')
            return render(request, 'registration/login.html',
                          context={'error': form.errors, 'google_client_id': GOOGLE_CLIEND_ID})
