from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Contas_Receber_Fgi
from .serializers import ContasAReceberSerializer
from .filters import ContasAReceberFilter
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class ContasAReceberPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class ContasAReceberViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    queryset = Contas_Receber_Fgi.objects.filter(
        Q(data_pagamento__isnull=True) | ~Q(data_pagamento='1900-01-01')
    ).order_by('data_vencimento')
    serializer_class = ContasAReceberSerializer
    pagination_class = ContasAReceberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContasAReceberFilter