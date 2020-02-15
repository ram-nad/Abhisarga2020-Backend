from django.shortcuts import render, redirect
from django.views import View
from .models import User, Profile
from .forms import ProfileEditForm, ProfileForm


class ProfileCreateView(View):
    def get(self, request):
        return render(request, 'registration/signup.html', context={'form': ProfileForm().as_p()})

    def post(self, request):
        form = ProfileForm(request.body)
        if form.is_valid():
            form.save()
            return redirect('home_page')
        else:
            print(form.errors)
            return render(request, 'registration/signup.html', context={})


