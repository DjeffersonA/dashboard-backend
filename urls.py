from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContasAReceberViewSet, ContasAPagarView, MetaAdsViewSet
from django.shortcuts import redirect

router = DefaultRouter()
router.register(r'ContasAReceber', ContasAReceberViewSet)
router.register(r'MetaAds', MetaAdsViewSet)

urlpatterns = [
    path('', lambda request: redirect('api/')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/ContasAPagar/', ContasAPagarView.as_view(), name='contas_a_pagar'),
]