from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from base.models import College
from .managers import UserManager
from .validators import validate_phone

gender_choices = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
)


class User(AbstractBaseUser):
    email = models.EmailField(blank=False, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        if self.is_superuser or self.is_staff:
            return True
            # return self.profile.volunteer.is_administrator
        else:
            return False

    def has_module_perms(self, app_label):
        if self.is_superuser or self.is_staff:
            return True
            # return self.profile.volunteer.is_administrator
        else:
            return False

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_volunteer(self):
        if hasattr(self, 'profile'):
            return hasattr(self.profile, "volunteer")
        else:
            return False

    @property
    def name(self):
        return self.profile.first_name + " " + self.profile.last_name

    @property
    def college(self):
        return self.profile.college

    @property
    def gender(self):
        return self.profile.gender


class Profile(models.Model):
    user = models.OneToOneField(to=User, related_name="profile", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    college = models.ForeignKey(to=College, related_name='students', on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=13, blank=True, validators=[validate_phone], unique=True)
    profile_pic = models.ImageField(upload_to="profilepics", default="profilepics/default_profile_pic.jpg")
    gender = models.CharField(max_length=1, choices=gender_choices)

    def __str__(self):
        return self.first_name + " " + self.last_name + "(" + self.user.email + ")"

    @property
    def name(self):
        return self.first_name + " " + self.last_name

    @property
    def is_volunteer(self):
        return hasattr(self, 'volunteer')

    def clean(self):
        super().clean()
        self.phone_number = validate_phone(self.phone_number)


class Volunteer(models.Model):
    profile = models.OneToOneField(to=Profile, related_name="volunteer", on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    fb = models.URLField(verbose_name="Facebook Profile", blank=True)
    linkedin = models.URLField(verbose_name="LinkedIn Profile", blank=True)
    insta = models.URLField(verbose_name="Instagram Profile", blank=True)
    is_administrator = models.BooleanField(default=False)

    @property
    def email(self):
        return self.profile.user.email

    @property
    def phone_number(self):
        return self.profile.phone_number

    @property
    def name(self):
        return self.profile.first_name + " " + self.profile.last_name

    @property
    def profile_pic(self):
        return self.profile.profile_pic
