from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve, Resolver404

PUBLIC_URL_NAMES = {
    'login',
    'logout',
    'home',
    'projetos',
    'servicos',
    'depoimentos',
    'contato',
}

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            return self.get_response(request)

        path = request.path_info

        if request.path.startswith(settings.STATIC_URL):
            return self.get_response(request)

        if request.path.startswith('/admin'):
            return self.get_response(request)

        if getattr(settings, 'MEDIA_URL', None):
            media_url = settings.MEDIA_URL.rstrip('/')
            if media_url and media_url != '/':
                if path.startswith(media_url + '/'):
                    return self.get_response(request)

        try:
            resolved = resolve(request.path)
            current_url = resolved.url_name
        except Resolver404:
            return self.get_response(request)

        if current_url in PUBLIC_URL_NAMES:
            return self.get_response(request)

        return redirect(settings.LOGIN_URL)
