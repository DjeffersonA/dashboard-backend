from rest_framework import serializers
from .models import Contas_Receber_Fgi, MetaAdsData

class ContasAReceberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contas_Receber_Fgi
        fields = '__all__'

class MetaAdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaAdsData
        fields = '__all__'