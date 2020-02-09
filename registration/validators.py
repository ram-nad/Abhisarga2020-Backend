import re

from django.core.exceptions import ValidationError


def validate_phone(phone_number):
    pattern = re.compile(r'^((\+[1-9][0-9])|(0))?[1-9][0-9]{9}')
    if not pattern.match(phone_number):
        raise ValidationError("Phone number is invalid.")
    else:
        if len(phone_number) == 11:
            return "+91" + phone_number[1:]
        elif len(phone_number) == 13:
            return phone_number
        else:
            return "+91" + phone_number
