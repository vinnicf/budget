from rest_framework import serializers
from .models import Composition, CompositionComposition, CompositionInsumo, CostHistory

class CompositionInsumoSerializer(serializers.ModelSerializer):
    insumo_name = serializers.StringRelatedField(source='insumo.name')
    insumo_codigo = serializers.StringRelatedField(source='insumo.codigo')
    insumo_cost = serializers.StringRelatedField(source='insumo.currentcost')
    insumo_unit = serializers.StringRelatedField(source='insumo.unit')

    class Meta:
        model = CompositionInsumo
        fields = ('insumo_name','insumo_codigo', 'insumo_cost', 'quantity','insumo_unit')

class CompositionCompositionSerializer(serializers.ModelSerializer):
    composition_name = serializers.StringRelatedField(source='child_composition.name')
    composition_codigo = serializers.StringRelatedField(source='child_composition.codigo')
    composition_cost = serializers.StringRelatedField(source='child_composition.total_cost')
    composition_unit = serializers.StringRelatedField(source='child_composition.unit')
    
    
    class Meta:
        model = CompositionComposition
        fields = ('composition_name', 'composition_codigo', 'quantity', 'composition_unit', 'composition_cost')




class CompositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composition
        fields = '__all__'


class CompositionDetailSerializer(serializers.ModelSerializer):
    compositioninsumo_set = CompositionInsumoSerializer(many=True, read_only=True)
    compositionchild_set = CompositionCompositionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Composition
        fields = ('id', 'codigo', 'name', 'unit', 'comp_cost', 'compositioninsumo_set', 'compositionchild_set')
        depth = 1


class CostHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CostHistory
        fields = '__all__'



