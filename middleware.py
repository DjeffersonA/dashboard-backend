from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import BasePermission, SAFE_METHODS

class RedirectToAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if request.path.startswith('/admin/') or (
                request.path.startswith('/api/ContasAReceber/') and request.GET.get('format') == 'json'
            ) or (
                request.path.startswith('/api/ContasAPagar/') and request.GET.get('format') == 'json'
            ):
                return self.get_response(request)
            return redirect('/admin/')
        
        response = self.get_response(request)
        return response