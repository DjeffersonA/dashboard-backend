from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

class RedirectToAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path.startswith('/api/'):
            return redirect('/admin/')
        response = self.get_response(request)
        return response