from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContasAReceberViewSet
from django.shortcuts import redirect

router = DefaultRouter()
router.register(r'ContasAReceber', ContasAReceberViewSet)

urlpatterns = [
    path('', lambda request: redirect('api/')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]