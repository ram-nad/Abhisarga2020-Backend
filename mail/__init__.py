from django.core.mail import send_mail, send_mass_mail

from .mailgun import send_mail as mailgun_send_mail, send_mass_mail as mailgun_send_mass_mail

smtp_send_mail = send_mail
smtp_send_mass_mail = send_mass_mail
