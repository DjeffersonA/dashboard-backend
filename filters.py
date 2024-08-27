import django_filters
from .models import Contas_Receber_Fgi

class ContasAReceberFilter(django_filters.FilterSet):
    data_inicio = django_filters.DateFilter(field_name='data_vencimento', lookup_expr='gte')
    data_fim = django_filters.DateFilter(field_name='data_vencimento', lookup_expr='lte')

    class Meta:
        model = Contas_Receber_Fgi
        fields = ['data_inicio', 'data_fim']