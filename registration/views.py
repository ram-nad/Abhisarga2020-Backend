from django.contrib.auth import authenticate, login as auth_login
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View

from AbhisargaBackend.settings import GOOGLE_CLIENT_ID, NEXT_PARAMETER
from AbhisargaBackend.settings import URL
from base.models import College
from mail import send_mail
from .forms import ProfileForm, LoginForm, gender_choices
from .models import User
from .token import registration_token_generator, get_user_google


def create_user_return_token(email):
    u = User.objects.get_or_none(email=email)
    if u is None:
        new_user = User.objects.create(email=email)
        new_user.set_password(None)
        new_user.full_clean()
        new_user.save()
        user_token = registration_token_generator.make_token(new_user)
        return user_token
    elif not u.is_active:
        user_token = registration_token_generator.make_token(u)
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
                token = create_user_return_token(email)
                if token is not None:
                    url = URL + reverse('profile_create', args=[email, token])
                    html = render_to_string('email/account_generation.html', context={'title': "Email Confirmation",
                                                                                      'head': "Email Verification",
                                                                                      'name': "User",
                                                                                      'action': {
                                                                                          'name': "Verify My Email",
                                                                                          'href': url}})
                    text = "Please open the link given below to verify your email for Abhisarga 2020. \n" + url + \
                           "\nIf you did not request registration for Abhisarga 2020 then please ignore this email." + \
                           "\nRegards,\nAbhisarga 2020 Team"
                    if send_mail("Email Verification for Abhisarga 2020", text, html, [email]) is not None:
                        return render(request, 'base/message.html',
                                      context={'title': "Verification Link sent.",
                                               'message': 'Email Verification link sent, please check your email. '
                                                          'The link is valid for next 1 hour.',
                                               'next': {'url': reverse('home'), 'name': "Go Back Home"}})
                    else:
                        return render(request, 'registration/signup.html',
                                      context={'error': 'Registration Failed, please try again later.',
                                               'google_client_id': GOOGLE_CLIENT_ID})
                else:
                    return render(request, 'registration/signup.html',
                                  context={'error': 'User already registered',
                                           'google_client_id': GOOGLE_CLIENT_ID})

        except (KeyError, ValueError, ValidationError):
            return render(request, 'registration/signup.html',
                          context={'error': 'Invalid Request', 'google_client_id': GOOGLE_CLIENT_ID})


def login_and_redirect(request, user):
    auth_login(request, user)
    if NEXT_PARAMETER in request.GET:
        return redirect(request.GET[NEXT_PARAMETER])
    else:
        return redirect('home')


def profile_create_get(request, email, token):
    u = User.objects.get_or_none(email=email)
    if u is None or u.is_active:
        return HttpResponseBadRequest()
    elif not registration_token_generator.check_token(u, token):
        return HttpResponseBadRequest()
    else:
        return render(request, 'registration/signup_full.html',
                      context={'email': email, 'token': token, 'colleges': College.objects.all(),
                               'gender': gender_choices})


def profile_create_post(request):
    email = request.POST['email']
    token = request.POST['token']
    u = User.objects.get_or_none(email=email)
    if u is None or u.is_active or not registration_token_generator.check_token(u, token):
        return HttpResponseBadRequest()
    else:
        pf = ProfileForm(request.POST, request.FILES)
        if pf.is_valid():
            try:
                pf.save()
                return login_and_redirect(request, u)
            except ValidationError as e:
                return render(request, 'registration/signup_full.html',
                              context={'email': email, 'token': token, 'colleges': College.objects.all(),
                                       'gender': gender_choices,
                                       'error': e.error_dict})
        else:
            return render(request, 'registration/signup_full.html',
                          context={'email': email, 'token': token, 'colleges': College.objects.all(),
                                   'gender': gender_choices,
                                   'error': pf.errors})


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
