from uuid import uuid4
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class UuidMiddleware:
    """
    Ajoute un id à chaque requête
    """
    def __init__(self, get_response):
        self.get_response = get_response



    def __call__(self, request):
        request.uuid = str(uuid4())
        return self.get_response(request)


class DomainMiddleware:
    """
    Ajoute le chemin du site à l'objet requesr
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cactus_domain = "%s://%s/" % (request.scheme, request.get_host())

        if settings.EXTRA_DOMAIN_PATH:
            cactus_domain = cactus_domain + settings.EXTRA_DOMAIN_PATH

        request.cactus_domain = cactus_domain

        return self.get_response(request)


class SuperUserRedirectMiddleware:
    """
    redirige les super utilisateurs loggé vers la page admin
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        redirect_url = "/admin/"
        print(request.path)

        if request.user.is_authenticated and request.user.is_superuser and request.path[:7] != redirect_url:
            return redirect(redirect_url)

        return self.get_response(request)