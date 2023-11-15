from rest_framework import serializers
from .models import Orcamento, OrcamentoItem



class OrcamentoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrcamentoItem
        fields = '__all__'


class OrcamentoSerializer(serializers.ModelSerializer):
    items = OrcamentoItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Orcamento
        fields = '__all__'
        read_only_fields = ('user',)