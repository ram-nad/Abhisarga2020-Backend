from django import forms
from django.db import transaction
from django.forms.utils import ErrorList

from base.models import College
from .models import Profile, User, gender_choices
from .validators import validate_phone


class ProfileForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50, required=False)
    college = forms.ModelChoiceField(queryset=College.objects)
    phone_number = forms.CharField(max_length=13, required=False, validators=[validate_phone])
    gender = forms.ChoiceField(choices=gender_choices)
    profile_pic = forms.ImageField(required=False)

    @transaction.atomic()
    def save(self, commit=True):
        if self.is_valid():
            print(self.errors)
            user = User(email=self.cleaned_data.get('email'))
            user.set_password(self.cleaned_data.get('password'))
            user.full_clean()
            user.save()
            self.cleaned_data.pop('email')
            self.cleaned_data.pop('password')
            if self.cleaned_data.get('profile_pic') is None:
                self.cleaned_data.pop('profile_pic')
            profile = Profile(user=user, **self.cleaned_data)
            profile.full_clean()
            profile.save()
            return profile
        else:
            raise ValueError("Could not save data.")


class ProfileEditForm(forms.ModelForm):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None, use_required_attribute=None,
                 renderer=None):
        if instance is None:
            raise ValueError("Instance must be provided to use this form.")
        else:
            super().__init__(self, data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted,
                             use_required_attribute, renderer)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'college', 'phone_number', 'gender', 'profile_pic']


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
