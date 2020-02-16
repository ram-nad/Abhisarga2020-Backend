import requests
from django.conf import settings


def send_mail(subject, body, to, sender=settings.MAILGUN_HOST_USER, fail_silently=True, body_type='html'):
    """
    Send a Single mail to one or more users

    Parameters:  \n
        subject (str): Subject of the email
        body (str): Body of the email
        to (list(str)): List of Recipients email address
        from (str): (optional) The Address from which the mail is sent
        body_type(str): (optional) choose if the mail will be text or HTML
    Returns:
        returns a response object
    """
    try:
        response = requests.post(
            settings.MAILGUN_BASE_URL,
            auth=('api', settings.MAILGUN_API_KEY),
            data={'from': sender,
                  'to': to,
                  'subject': subject,
                  body_type: body
                  })
    except:
        if not fail_silently:
            print('Unable to Send Post Request')
            return None
    if not fail_silently and response.status_code != 200:
        print("Unable to Send Mail")

    return response


def send_mass_mail(data_tuples, fail_silently=True, body_type='html'):
    """
    Send a Collection of mails

    Parameters:\n
        data_tuples (tuple): A tuple of tuples having the following parameters in order

    Format of data_tuple element:\n
        subject (str): Subject of the email
        body (str): Body of the email
        to (list(str)): List of Recipients email address
        from (str): (optional) The Address from which the mail is sent
        body_type(str): (optional) choose if the mail will be text or HTML

    Returns:
        returns a response object
    """

    with requests.Session() as my_session:
        my_session.auth = ('api', settings.MAILGUN_API_KEY)
        for mail in data_tuples:
            if len(mail) == 3:
                subject, body, to = mail
                sender = settings.MAILGUN_HOST_USER
            elif len(mail) == 4:
                subject, body, to, sender = mail
            else:
                print("Mail Not Sent: Incomplete Arguments")
                continue
            try:
                response = my_session.post(
                    settings.MAILGUN_BASE_URL,
                    data={'from': sender,
                          'to': to,
                          'subject': subject,
                          body_type: body})
                if not fail_silently and response.status_code != 200:
                    print('Cannot send mail.')
            except:
                if not fail_silently:
                    print('Unable to Send Post Request')
