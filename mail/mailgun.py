import requests
from django.conf import settings


def send_mail(subject, message, html_message, recipient_list, from_email=settings.MAILGUN_HOST_USER,
              fail_silently=True):
    """
    Returns:
        Response Object or None if failed
    """
    try:
        response = requests.post(
            settings.MAILGUN_BASE_URL,
            auth=('api', settings.MAILGUN_API_KEY),
            data={'from': from_email,
                  'to': recipient_list,
                  'subject': subject,
                  'text': message,
                  'html': html_message
                  })
        if not fail_silently and response.status_code != 200:
            print("Unable to send Mailgun Mail.")

        return response
    except:
        if not fail_silently:
            print('Unable to Send Post Request')
            return None


def send_mass_mail(data_tuples, fail_silently=True):
    """
    Returns:
        Response Object or None if failed
    """
    with requests.Session() as my_session:
        my_session.auth = ('api', settings.MAILGUN_API_KEY)
        for mail in data_tuples:
            if len(mail) == 3:
                subject, message, html_message, recipient_list = mail
                from_email = settings.MAILGUN_HOST_USER
            elif len(mail) == 4:
                subject, message, html_message, recipient_list, from_email = mail
            else:
                print("Mailgun Mail Not Sent: Incomplete Arguments")
                continue
            try:
                response = my_session.post(
                    settings.MAILGUN_BASE_URL,
                    data={'from': from_email,
                          'to': recipient_list,
                          'subject': subject,
                          'text': message,
                          'html': html_message})
                if not fail_silently and response.status_code != 200:
                    print('Cannot send Mailgun Mail.')
            except:
                if not fail_silently:
                    print('Unable to Send Post Request')
