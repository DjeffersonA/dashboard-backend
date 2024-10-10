from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Contas_Receber_Fgi, MetaAdsData
from .serializers import ContasAReceberSerializer, MetaAdsSerializer
from .filters import ContasAReceberFilter, MetaAdsFilter
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .authSheets import authSheets
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import threading
import requests
import environ, os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

class Pagination(PageNumberPagination):
    page_size = 10000
    page_size_query_param = 'page_size'
    max_page_size = 100000

class MetaAdsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = MetaAdsData.objects.all().order_by('date_start')
    serializer_class = MetaAdsSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MetaAdsFilter

    def request_rep(self):
        all_data = [] 
        
        url = (
            f"https://graph.facebook.com/v20.0/act_{env('FB_AD_ACCOUNT_ID')}/insights"
            f"?level={env('FB_LEVEL')}&fields={env('FB_FIELDS')}&time_increment=1"
            f"&date_preset=this_month"
            f"&access_token={env('FB_TOKEN')}"
        )

        while url:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            all_data.extend(item for item in data.get('data', []) if item.get('campaign_name') or item.get('adset_name'))
            url = data.get('paging', {}).get('next')

        return all_data
    
    def import_db(self, data):
        for row in data:
            MetaAdsData.objects.update_or_create(
                campaign_name=row['campaign_name'],
                adset_name=row['adset_name'],
                date_start=row['date_start'],
                date_stop=row['date_stop'],
                defaults={'spend': row['spend']},
            )
    
    @method_decorator(cache_page(60*60*6))
    def list(self, request, *args, **kwargs):
        data = self.request_rep()
        self.import_db(data)
        
        cache_key = f"metaads_{request.query_params}"
        response_data = cache.get(cache_key)

        if response_data is None:
            response = super().list(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=60*60*6)  # Cache de 6 horas
            response_data = response.data
        else:
            threading.Thread(target=lambda: self.refresh_cache(request, cache_key, *args, **kwargs)).start()
        
        return Response(response_data)
    
    def refresh_cache(self, request, cache_key, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60*60*6)  # Cache de 6 horas
        

class ContasAReceberViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Contas_Receber_Fgi.objects.filter(
        Q(data_pagamento__isnull=True) | ~Q(data_pagamento='1900-01-01')
    ).order_by('data_vencimento')
    serializer_class = ContasAReceberSerializer
    pagination_class = Pagination
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
    
    @method_decorator(cache_page(60*60*24))  # Cache de 1 dia
    def list(self, request, *args, **kwargs):
        cache_key = f"contasareceber_{request.query_params}"
        response_data = cache.get(cache_key)

        if response_data is None:
            response = super().list(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=60*60*24)  # Cache de 1 dia
            response_data = response.data
        else:
            threading.Thread(target=lambda: self.refresh_cache(request, cache_key, *args, **kwargs)).start()

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
    
    def refresh_cache(self, request, cache_key, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60*60*24)  # Cache de 1 dia
    
class ContasAPagarView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')

        if data_inicio:
            data_inicio = data_inicio.replace('-', '/')
        if data_fim:
            data_fim = data_fim.replace('-', '/')

        start_date = datetime.strptime(data_inicio, "%d/%m/%Y") if data_inicio else None
        end_date = datetime.strptime(data_fim, "%d/%m/%Y") if data_fim else None

        sheet_keys = [
            "1fbWfjEo5jmi9FeNtYyYo_IK6J-zojbwervOATmi56_8",
            "1iiz5IzrHMxfYRFBcp-0145_LVBZRObpMaOvMv1L46xQ"
        ]
        
        all_data = []

        for key in sheet_keys:
            cache_key = f"contasapagar_{key}_{data_inicio}_{data_fim}"
            cached_data = cache.get(cache_key)

            if cached_data is None:
                gc = authSheets()
                sheet = gc.open_by_key(key)
                worksheet = sheet.worksheet("Looker")
                data = worksheet.get_all_records()

                # Cache de 15 minutos
                cache.set(cache_key, data, timeout=60*15)
                cached_data = data

            all_data.extend(cached_data) 

        if start_date and end_date:
            filtered_data = [
                item for item in all_data
                if 'Data' in item and item['Data'] != "" and start_date <= datetime.strptime(item['Data'], "%d/%m/%Y") <= end_date
            ]
        else:
            filtered_data = all_data

        return Response(filtered_data)