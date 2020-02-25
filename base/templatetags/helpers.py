from django import template

register = template.Library()


@register.filter(name='times')
def times(value):
    return list(range(value))


@register.filter(name="has_attr")
def has_attr(obj, attr):
    return hasattr(obj, attr)


@register.filter(name="get_obj_attr")
def get_obj_attr(obj, attr):
    return getattr(obj, attr)
