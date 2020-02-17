from smtplib import SMTPException

from django.core.mail import send_mail, get_connection, EmailMultiAlternatives

from AbhisargaBackend.settings import EMAIL_HOST_USER, USE_MAILGUN, MAILGUN_HOST_USER
from .mailgun import send_mail as mailgun_send_mail, send_mass_mail as mailgun_send_mass_mail


def smtp_send_mail(subject, message, html_message, recipient_list, from_email=EMAIL_HOST_USER, fail_silently=True):
    """
    Returns:
        Number of mail sent successfully or None if failed
    """
    try:
        return send_mail(subject, message, from_email, recipient_list, fail_silently, None, None, None, html_message)
    except SMTPException:
        if not fail_silently:
            print("Unable to send SMTP Mail.")
        return None


def smtp_send_mass_mail(data_tuples, fail_silently=True):
    """
    Returns:
        Number of mail sent successfully or None if failed
    """
    connection = get_connection(username=None, password=None, fail_silently=fail_silently)
    messages = []
    for data in data_tuples:
        if len(data) == 4:
            subject, message, html_message, recipient_list = data
            from_email = EMAIL_HOST_USER
        elif len(data) == 5:
            subject, message, html_message, recipient_list, from_email = data
        else:
            print("SMTP Mail not send: too few or too many arguments.")
            continue
        message = EmailMultiAlternatives(subject, message, from_email, recipient_list)
        message.attach_alternative(html_message, 'text/html')
        messages.append(message)
    try:
        return connection.send_messages(messages)
    except SMTPException:
        if not fail_silently:
            print("Unable to send SMTP Mail.")
        return None


def send_mail(subject, message, html_message, recipient_list, from_email=None, fail_silently=True):
    """
        Send a Single mail to one or more users

        Parameters:  \n
            subject (str): Subject of the email
            message (str): Body of the email (text)
            html_message (str): Body of HTML message
            recipient_list (list(str)): List of Recipients email address
            from_email (str): (optional) The Address from which the mail is sent
            [uses EMAIL_HOST_USER for SMTP by default and MAILGUN_HOST_USER for mailgun by default.]
        Returns:
            returns None if failed, on success return type depends upon whether SMTP is used or Mailgun
    """
    if USE_MAILGUN:
        if not from_email:
            from_email = MAILGUN_HOST_USER
        return mailgun_send_mail(subject, message, html_message, recipient_list, from_email, fail_silently)
    else:
        if not from_email:
            from_email = EMAIL_HOST_USER
        return smtp_send_mail(subject, message, html_message, recipient_list, from_email, fail_silently)


def send_mass_mail(data_tuples, fail_silently=True):
    """
    Send a Collection of mails

    Parameters:\n
        data_tuples (tuple): A tuple of tuples having the following parameters in order

    Format of data_tuples element:\n
        subject (str): Subject of the email
        message (str): Body of the email (text)
        html_message (str): Body of HTML message
        recipient_list (list(str)): List of Recipients email address
        from_email (str): (optional) The Address from which the mail is sent
        [uses EMAIL_HOST_USER for SMTP by default and MAILGUN_HOST_USER for mailgun by default.]
    Returns:
        returns None if failed, on success return type depends upon whether SMTP is used or Mailgun
    """
    if USE_MAILGUN:
        return mailgun_send_mail(data_tuples, fail_silently)
    else:
        return smtp_send_mail(data_tuples, fail_silently)
