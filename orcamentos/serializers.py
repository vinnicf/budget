from rest_framework import serializers
from .models import Orcamento, OrcamentoItem



class OrcamentoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrcamentoItem
        fields = '__all__'


class OrcamentoSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    
    class Meta:
        model = Orcamento
        fields = '__all__'
        read_only_fields = ('user',)

    def get_items(self, obj):
        # Check if the request is a detail view
        if self.context['view'].action == 'retrieve':
            # Detail view - include all items
            return OrcamentoItemSerializer(obj.items.all(), many=True).data
        # List view - do not include items or include limited data
        return None  # Or return limited data