from django.shortcuts import render


def home(request):
    return render(request, 'base/home.html')


def contact(request):
    return render(request, 'home/contact.html')


def permission_denied(request, exception, *args, **kwargs):
    return render(request, 'error/403.html', status=403, context={'details': str(exception)})


def internal_server_error(request, *args, **kwargs):
    return render(request, 'error/500.html', status=500)


def not_found(request, exception, *args, **kwargs):
    text = str(request.path) + " not found on this server."
    return render(request, 'error/404.html', status=404, context={'details': text})


def bad_request(request, exception, *args, **kwargs):
    return render(request, 'error/400.html', status=400)
