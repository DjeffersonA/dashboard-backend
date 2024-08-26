from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Contas_Receber_Fgi
from .serializers import ContasReceberSerializer
from .filters import ContasReceberFilter

class ContasReceberPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class ContasReceberViewSet(viewsets.ModelViewSet):
    queryset = Contas_Receber_Fgi.objects.all()
    serializer_class = ContasReceberSerializer
    pagination_class = ContasReceberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContasReceberFilter