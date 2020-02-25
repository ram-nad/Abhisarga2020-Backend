from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_encode as b64_encode, urlsafe_base64_decode as b64_decode
from django.views import View

from AbhisargaBackend.settings import GOOGLE_CLIENT_ID, NEXT_PARAMETER
from AbhisargaBackend.settings import URL
from base.models import College
from base.views import bad_request
from mail import send_mail
from .forms import ProfileForm, LoginForm, gender_choices
from .models import User, Volunteer
from .token import registration_token_generator, get_user_google, password_token_generator


def create_user_return_token(email):
    u = User.objects.get_or_none(email=email)
    if u is None:
        new_user = User.objects.create(email=email)
        new_user.set_password(None)
        new_user.full_clean()
        new_user.save()
        user_token = registration_token_generator.make_token(new_user)
        b64id = b64_encode(bytes(str(new_user.pk).encode()))
        return [user_token, b64id]
    elif not u.is_active:
        user_token = registration_token_generator.make_token(u)
        b64id = b64_encode(bytes(str(u.pk).encode()))
        return [user_token, b64id]
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
                    tokens = create_user_return_token(email)
                    if tokens is not None:
                        return redirect('profile_create', b64id=tokens[1], token=tokens[0])
                    else:
                        return render(request, 'registration/signup.html',
                                      context={'error': 'User already registered',
                                               'google_client_id': GOOGLE_CLIENT_ID})
            else:
                email = request.POST['email']
                tokens = create_user_return_token(email)
                if tokens is not None:
                    url = URL + reverse('profile_create', args=[tokens[1], tokens[0]])
                    html = render_to_string('email/account_generation.html', context={'title': "Email Confirmation",
                                                                                      'head': "Email Verification",
                                                                                      'name': "User",
                                                                                      'action': {
                                                                                          'name': "Verify My Email",
                                                                                          'href': url}})
                    text = "Please open the link given below to verify your email for Abhisarga 2020. \n" + url + \
                           "\nIf you did not request registration for Abhisarga 2020 then please ignore this email." + \
                           "\nRegards,\nAbhisarga 2020 Team"
                    send_mail("Email Verification for Abhisarga 2020", text, html, [email])
                    return render(request, 'base/message.html',
                                  context={'title': "Verification Link sent",
                                           'message': 'Email Verification link will be sent shortly, please '
                                                      'check your email. '
                                                      'The link is valid for next 1 hour.',
                                           'next': {'url': reverse('home'), 'name': "Go Back Home"}})
                else:
                    return render(request, 'registration/signup.html',
                                  context={'error': 'User already registered',
                                           'google_client_id': GOOGLE_CLIENT_ID})

        except (KeyError, ValueError, ValidationError):
            return render(request, 'registration/signup.html',
                          context={'error': 'Invalid Request', 'google_client_id': GOOGLE_CLIENT_ID})


def login_and_redirect(request, user):
    if not user.is_active:
        return bad_request(request, None)
    auth_login(request, user)
    if NEXT_PARAMETER in request.GET:
        return redirect(request.GET[NEXT_PARAMETER])
    else:
        return redirect('home')


def profile_create_get(request, b64id, token):
    pk = b64_decode(b64id).decode()
    u = User.objects.get_or_none(pk=pk)
    if u is None or u.is_active:
        return bad_request(request, None)
    elif not registration_token_generator.check_token(u, token):
        return bad_request(request, None)
    else:
        return render(request, 'registration/signup_full.html',
                      context={'email': u.email, 'token': token, 'colleges': College.objects.all()[:8],
                               'gender': gender_choices})


def profile_create_post(request):
    email = request.POST.get('email', None)
    token = request.POST.get('token', None)
    if email is None or token is None:
        return bad_request(request, None)
    u = User.objects.get_or_none(email=email)
    if u is None or u.is_active or not registration_token_generator.check_token(u, token):
        return bad_request(request, None)
    else:
        pf = ProfileForm(request.POST, request.FILES)
        if pf.is_valid():
            password = pf.cleaned_data.get('password')
            try:
                pf.save()
                new_user = authenticate(email=email, password=password)
                return login_and_redirect(request, new_user)
            except ValidationError as e:
                return render(request, 'registration/signup_full.html',
                              context={'email': email, 'token': token, 'colleges': College.objects.all()[:8],
                                       'gender': gender_choices,
                                       'error': e.message_dict})
        else:
            return render(request, 'registration/signup_full.html',
                          context={'email': email, 'token': token, 'colleges': College.objects.all()[:8],
                                   'gender': gender_choices,
                                   'error': pf.errors})


class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(to='home')
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


class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return redirect(to='home')


class PasswordChangeView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = NEXT_PARAMETER

    def get(self, request):
        return render(request, 'registration/change_password.html')

    def post(self, request):
        try:
            old_pass, new_pass, conf_new_pass = request.POST[
                                                    'old'], request.POST['password1'], request.POST['password2']
        except KeyError:
            return render(request, 'registration/change_password.html', context={'error': 'Some fields are missing.'})
        if request.user.check_password(old_pass):
            if new_pass == conf_new_pass:
                request.user.set_password(new_pass)
                context = {"title": "Password Updated",
                           "message": "Password Changed Successful",
                           "next": {"url": reverse('home'), "name": 'Go back to home'}}
                return render(request, 'base/message.html',
                              context=context)
            else:
                error = "New passwords do not match."
                return render(request, 'registration/change_password.html', context={'error': error})
        else:
            error = "Old password is wrong."
            return render(request, 'registration/change_password.html', context={'error': error})


class PasswordResetView(View):
    def get(self, request):
        return render(request, 'registration/forgot_password.html')


class PasswordResetDoneView(View):
    def post(self, request):
        dtg = password_token_generator
        try:
            email = request.POST['email']
            user = User.objects.get_or_none(email=email)
            if user is None or not user.is_active:
                error = 'No account found with that Email-id.'
                return render(request, 'registration/forgot_password.html', context={'error': error})
        except KeyError:
            error = 'Please enter your Email.'
            return render(request, 'registration/forgot_password.html', context={'error': error})
        token = dtg.make_token(user)
        idb64 = b64_encode(bytes(str(user.pk).encode()))
        url = URL + reverse('password_reset_confirm', args=[idb64, token])
        html = render_to_string('email/password_reset.html', context={'title': "Reset Password",
                                                                      'head': "Reset Password",
                                                                      'name': user.name,
                                                                      'action': {
                                                                          'name': "Reset my Password",
                                                                          'href': url}})
        text = "Please open the link given below to reset password for your Abhisarga 2020 account. \n" + url + \
               "\nIf you did not request password reset then please ignore this email." + \
               "\nRegards,\nAbhisarga 2020 Team"
        send_mail("Password Reset for Abhisarga 2020", text, html, [email])
        message = {"title": "Password Reset Confirmation",
                   "message": "An mail will be sent to your registered email with the link to reset"
                              " your password, shortly.",
                   "next": {"url": reverse('login'), "name": 'Return to Login Page'}}
        return render(request, 'base/message.html', context=message)


class PasswordResetConfirmView(View):
    def get(self, request, idb64, token):
        dtg = password_token_generator
        user = User.objects.get_or_none(pk=b64_decode(idb64).decode())
        if user is None:
            return bad_request(request, None)
        if dtg.check_token(user, token):
            return render(request, 'registration/reset_password.html', context={'idb64': idb64, 'token': token})
        return bad_request(request, None)


class PasswordResetCompleteView(View):
    def post(self, request):
        try:
            idb64 = request.POST['idb64']
            token = request.POST['token']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            user = User.objects.get(pk=b64_decode(idb64).decode())
            if password1 != password2:
                raise ValueError
            dtg = password_token_generator
            if not dtg.check_token(user, token):
                raise AssertionError
        except KeyError:
            return bad_request(request, None)
        except ValueError:
            return bad_request(request, None)
        except User.DoesNotExist:
            return bad_request(request, None)
        except AssertionError:
            return bad_request(request, None)

        user.set_password(password1)
        user.save()
        message = {"title": "Password reset successful",
                   "message": "Your password has been updated successfully.",
                   "next": {"url": reverse('login'), "name": 'Return to Login Page'}}
        return render(request, 'base/message.html', context=message)


class VolunteerView(View):
    def get(self, request):
        return render(request, 'base/members.html', context={'volunteers': Volunteer.objects.all()})


class UserProfile(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = NEXT_PARAMETER

    def get(self, request):
        return render(request, 'registration/profile.html', context={'profile': request.user.profile})
