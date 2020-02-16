from django.core.exceptions import PermissionDenied


def volunteer_access(func):
    def inner_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_volunteer:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied('Only volunteers can access this page.')

    return inner_func


def administrator_access(func):
    def inner_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_volunteer:
            if request.user.profile.volunteer.is_administrator:
                return func(request, *args, **kwargs)
        raise PermissionDenied('Only administrators can access this page.')

    return inner_func
