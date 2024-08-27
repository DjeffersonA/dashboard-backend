from rest_framework import serializers
from .models import Contas_Receber_Fgi

class ContasAReceberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contas_Receber_Fgi
        fields = '__all__'