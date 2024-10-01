from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Contas_Receber_Fgi
from .serializers import ContasAReceberSerializer
from .filters import ContasAReceberFilter
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
import gspread
from .authSheets import authSheets
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class ContasAReceberPagination(PageNumberPagination):
    page_size = 10000
    page_size_query_param = 'page_size'
    max_page_size = 100000

class ContasAReceberViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Contas_Receber_Fgi.objects.filter(
        Q(data_pagamento__isnull=True) | ~Q(data_pagamento='1900-01-01')
    ).order_by('data_vencimento')
    serializer_class = ContasAReceberSerializer
    pagination_class = ContasAReceberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContasAReceberFilter

    def format_date(self, date_str):
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
            except ValueError:
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    return date_str
            return date_obj.strftime("%d-%m-%Y")
        return None
    
    @method_decorator(cache_page(60*15))  # Cache de 15 minutos
    def list(self, request, *args, **kwargs):
        cache_key = f"contasareceber_{request.query_params}"
        response_data = cache.get(cache_key)

        if response_data is None:
            response = super().list(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=60*15)  # Cache de 15 minutos
            response_data = response.data

        import_param = request.query_params.get('import', '1')
        if import_param == '1':
            gc = authSheets()
            sheet = gc.open_by_key("1WOeOBWwDumY5hIF1zgkDm-lw6DtjpqQBj6g8sfF38uk")
            worksheet = sheet.worksheet("DASHBOARD")
            
            header = [
                "ID Financeiro", "Matrícula", "Nome do Aluno", "CPF", "Telefone", "Email",
                "CNPJ Unidade", "Razão Social", "Formato", "Curso", "Período", 
                "Valor Mensalidade", "Data de Vencimento", "Valor Pago", 
                "Data de Pagamento", "Tipo de Parcela", "Tipo", "Número da Parcela", 
                "Situação do Contrato"
            ]

            worksheet.clear()
            worksheet.append_row(header, value_input_option="RAW")

            formatted_data = []
            for item in response_data['results']:
                formatted_data.append([
                    item.get("id_financeiro"),
                    item.get("matricula"),
                    item.get("nome_aluno"),
                    item.get("cpf"),
                    item.get("telefone"),
                    item.get("email"),
                    item.get("cnpj_unidade"),
                    item.get("razao_social"),
                    item.get("formato"),
                    item.get("curso"),
                    item.get("periodo"),
                    item.get("valor_mensalidade"),
                    self.format_date(item.get("data_vencimento")),
                    item.get("valor_pago"),
                    self.format_date(item.get("data_pagamento")),
                    item.get("tipo_parcela"),
                    item.get("tipo"),
                    item.get("numero_parcela"),
                    item.get("situacao_contrato"),
                ])

            worksheet.append_rows(formatted_data, value_input_option="RAW")

        return Response(response_data)
    
class ContasAPagarView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')

        cache_key = f"contasapagar_{data_inicio}_{data_fim}"
        cached_data = cache.get(cache_key)

        if cached_data is None:
            gc = authSheets()
            sheet = gc.open_by_key("1fbWfjEo5jmi9FeNtYyYo_IK6J-zojbwervOATmi56_8")
            worksheet = sheet.worksheet("Looker")
            data = worksheet.get_all_records()
            
            # Cache de 15 minutos
            cache.set(cache_key, data, timeout=60*15)
            cached_data = data

        return Response(cached_data)