from rest_framework import viewsets # type: ignore
from rest_framework.pagination import PageNumberPagination # type: ignore
from django_filters.rest_framework import DjangoFilterBackend # type: ignore
from .models import Contas_Receber_Fgi
from .serializers import ContasAReceberSerializer
from .filters import ContasAReceberFilter

class ContasAReceberPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class ContasAReceberViewSet(viewsets.ModelViewSet):
    queryset = Contas_Receber_Fgi.objects.all().order_by('data_vencimento')
    serializer_class = ContasAReceberSerializer
    pagination_class = ContasAReceberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContasAReceberFilter