from datetime import datetime

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from AbhisargaBackend.settings import GOOGLE_CLIENT_ID, PASSWORD_RESET_TIMEOUT, REGISTRATION_RESET_TIMEOUT


class PasswordTokenGenerator(PasswordResetTokenGenerator):

    def __init__(self, __timeout=PASSWORD_RESET_TIMEOUT):
        self.__timeout = __timeout
        super().__init__()

    def make_token(self, user):
        return self._make_token_with_timestamp(user, self._num_seconds(self._now()))

    def check_token(self, user, token):
        if not (user and token):
            return False
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False
        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False
        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            if not constant_time_compare(
                    self._make_token_with_timestamp(user, ts, legacy=True),
                    token,
            ):
                return False
        if (self._num_seconds(self._now()) - ts) > self.__timeout:
            return False

        return True

    def _num_seconds(self, dt):
        return int((dt - datetime(2001, 1, 1)).total_seconds())

    def _now(self):
        return datetime.now()


password_token_generator = PasswordTokenGenerator()


class RegistrationTokenGenerator(PasswordTokenGenerator):
    def __init__(self, __timeout=REGISTRATION_RESET_TIMEOUT):
        super().__init__(__timeout)

    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(user.email) + str(user.is_active) + str(timestamp)


registration_token_generator = RegistrationTokenGenerator()


def get_user_google(token):
    user = id_token.verify_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
    if user['iss'] not in ['accounts.google.com', 'https://accounts.google.com'] or 'email' not in user:
        raise ValueError('Wrong issuer.')
    else:
        return user
