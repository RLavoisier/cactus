from uuid import uuid4


class UuidMiddleware:
    """
    Ajoute un id à chaque requête
    """
    def __init__(self, get_response):
        self.get_response = get_response



    def __call__(self, request):
        request.uuid = str(uuid4())
        return self.get_response(request)