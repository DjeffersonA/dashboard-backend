import django_filters
from .models import Contas_Receber_Fgi, MetaAdsData

class ContasAReceberFilter(django_filters.FilterSet):
    data_inicio = django_filters.DateFilter(field_name='data_vencimento', lookup_expr='gte')
    data_fim = django_filters.DateFilter(field_name='data_vencimento', lookup_expr='lte')
    parcela_inicio = django_filters.NumberFilter(field_name='numero_parcela', lookup_expr='gte')
    parcela_fim = django_filters.NumberFilter(field_name='numero_parcela', lookup_expr='lte')

    class Meta:
        model = Contas_Receber_Fgi
        fields = ['data_inicio', 'data_fim', 'parcela_inicio', 'parcela_fim']

class MetaAdsFilter(django_filters.FilterSet):
    date_start = django_filters.DateFilter(field_name='date_start', lookup_expr='gte')
    date_stop = django_filters.DateFilter(field_name='date_stop', lookup_expr='lte')

    class Meta:
        model = MetaAdsData
        fields = ['date_start', 'date_stop']