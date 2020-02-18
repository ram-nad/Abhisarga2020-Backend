from django import template

register = template.Library()
from django.core.exceptions import NON_FIELD_ERRORS


def error_list(value):
    if isinstance(value, list):
        return ", ".join(value)
    elif isinstance(value, str):
        return value
    else:
        return ""


@register.filter(name='error_object')
def error_object(value):
    if isinstance(value, str):
        return value
    elif isinstance(value, dict):
        if NON_FIELD_ERRORS in value:
            return error_list(value)
        else:
            return ""
    else:
        return error_list(value)


register.filter('error_list', error_list)
