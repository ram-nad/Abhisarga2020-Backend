from django.http import HttpResponse
from django.shortcuts import render

from .models import College


def home(request):
    return render(request, 'base/home.html')


def permission_denied(request, exception, *args, **kwargs):
    return render(request, 'error/403.html', status=403, context={'details': str(exception)})


def internal_server_error(request, *args, **kwargs):
    return render(request, 'error/500.html', status=500)


def not_found(request, exception, *args, **kwargs):
    text = str(request.path) + " not found on this server."
    return render(request, 'error/404.html', status=404, context={'details': text})


def bad_request(request, exception, *args, **kwargs):
    return render(request, 'error/400.html', status=400)


def cancelled(request):
    return render(request, 'error/cancelled.html')


def get_college_list(request):
    college = request.GET.get('college', None)
    if college is None or str(college).strip() == '':
        return HttpResponse("", content_type="text/plain")
    colleges = College.objects.filter(name__icontains=college)[:8]
    text = "\n".join(list(map(lambda x: x.name, colleges)))
    return HttpResponse(text, content_type="text/plain")
