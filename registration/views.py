from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View

from AbhisargaBackend.settings import GOOGLE_CLIENT_ID, NEXT_PARAMETER
from .forms import *
from .token import registration_token_generator, get_user_google


def create_user_return_token(email):
    u = User.objects.get_or_none(email=email)
    if u is None or not u.is_active:
        new_user = User.objects.create(email=email)
        new_user.set_password(None)
        new_user.save()
        user_token = registration_token_generator.make_token(new_user)
        return user_token
    else:
        return None


class ProfileMakeView(View):
    def get(self, request):
        return render(request, 'registration/signup.html', context={'google_client_id': GOOGLE_CLIENT_ID})

    def post(self, request):
        try:
            if 'google-id-token' in request.POST:
                user = get_user_google(request.POST['google-id-token'])
                if user is None:
                    raise ValueError()
                else:
                    email = user['email']
                    token = create_user_return_token(email)
                    if token is not None:
                        return redirect('profile_create', email=email, token=token)
                    else:
                        return render(request, 'registration/signup.html',
                                      context={'error': 'User already registered',
                                               'google_client_id': GOOGLE_CLIENT_ID})
            else:
                email = request.POST['email']
                # token = create_user_return_token(email)
        except (KeyError, ValueError):
            return render(request, 'registration/signup.html',
                          context={'error': 'Invalid Request', 'google_client_id': GOOGLE_CLIENT_ID})


class ProfileCreateView(View):
    def get(self, request, email, token):
        u = User.objects.get_or_none(email=email)
        if u is None or u.is_active:
            return HttpResponseBadRequest()
        elif not registration_token_generator.check_token(u, token):
            return HttpResponseBadRequest()
        else:
            return render(request, 'registration/signup.html', context={'email': email, 'token': token})

    # def post(self, request):


def login_and_redirect(request, user):
    auth_login(request, user)
    if NEXT_PARAMETER in request.GET:
        return redirect(request.GET[NEXT_PARAMETER])
    else:
        return redirect('home')


class UserLoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html', context={'google_client_id': GOOGLE_CLIENT_ID})

    def post(self, request):
        if 'google-id-token' in request.POST:
            try:
                user = get_user_google(request.POST['google-id-token'])
                u = User.objects.get_or_none(email=user['email'])
                if u is None:
                    return render(request, 'registration/login.html',
                                  context={'error': 'User does not exist',
                                           'google_client_id': GOOGLE_CLIENT_ID})
                else:
                    return login_and_redirect(request, u)
            except ValueError:
                return render(request, 'registration/login.html',
                              context={'error': 'Invalid Login Attempt', 'google_client_id': GOOGLE_CLIENT_ID})
        else:
            form = LoginForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                email, password = data['email'], data['password']
                u = authenticate(request, email=email, password=password)
                if u is None:
                    return render(request, 'registration/login.html',
                                  context={'error': 'Wrong Email or Password',
                                           'google_client_id': GOOGLE_CLIENT_ID})
                return login_and_redirect(request, u)
            return render(request, 'registration/login.html',
                          context={'error': form.errors, 'google_client_id': GOOGLE_CLIENT_ID})
