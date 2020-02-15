from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View

from .forms import ProfileForm


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
                          context={'form': ProfileForm().as_p(), 'errors': form.errors})
