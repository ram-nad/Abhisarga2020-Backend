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
    email = models.EmailField(blank=False, unique=True, verbose_name="E-mail")
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        if self.is_superuser or self.is_staff:
            return True
        else:
            return False

    def has_module_perms(self, app_label):
        if self.is_superuser or self.is_staff:
            return True
        else:
            return False

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

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
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, blank=True, verbose_name="Last Name")
    college = models.ForeignKey(to=College, related_name='students', on_delete=models.SET_NULL, null=True,
                                verbose_name="College")
    phone_number = models.CharField(max_length=13, validators=[validate_phone], unique=True,
                                    verbose_name="Phone Number")
    profile_pic = models.ImageField(upload_to="profilepics", default="profilepics/default_profile_pic.jpg")
    gender = models.CharField(max_length=1, choices=gender_choices, verbose_name="Gender")

    def __str__(self):
        return self.first_name + " " + self.last_name + "(" + self.user.email + ")"

    @property
    def name(self):
        return self.first_name + " " + self.last_name

    @property
    def email(self):
        return self.user.email

    def clean(self):
        super().clean()
        self.phone_number = validate_phone(self.phone_number)

    class Meta:
        verbose_name = "Registrant"
        verbose_name_plural = "Registrants"


class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=False)
    phone_number = models.CharField(max_length=13, validators=[validate_phone])
    profile_pic = models.ImageField(upload_to="volunteer", default="volunteer/default_volunteer_pic.jpg")
    role = models.CharField(max_length=50)
    facebook = models.URLField(verbose_name="Facebook Profile", blank=True)
    linkedin = models.URLField(verbose_name="LinkedIn Profile", blank=True)
    instagram = models.URLField(verbose_name="Instagram Profile", blank=True)
    twitter = models.URLField(verbose_name="Twitter Profile", blank=True)

    def clean(self):
        super().clean()
        self.phone_number = validate_phone(self.phone_number)

    def __str__(self):
        return self.name + " (" + self.email + ")"
