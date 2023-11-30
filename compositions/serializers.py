from rest_framework import serializers
from .models import Composition, CompositionComposition, CompositionInsumo, CostHistory, Insumo

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
    total_cost = serializers.SerializerMethodField()
    material_cost = serializers.SerializerMethodField()
    mo_cost = serializers.SerializerMethodField()
    
    class Meta:
        model = Composition
        fields = ('id', 'codigo', 'name', 'unit', 'comp_cost', 'compositioninsumo_set', 'compositionchild_set', 'total_cost', 'material_cost', 'mo_cost')
        depth = 1

    def _calculate_costs_once(self, obj):
        if not hasattr(obj, '_cached_costs'):
            state = self.context.get('state', None)
            desonerado = self.context.get('desonerado', None)
            year_month = self.context.get('year_month', None)  # Get the date from the context
            obj._cached_costs = obj.calculate_cost(state=state, desonerado=desonerado, year_month=year_month)
        return obj._cached_costs

    def get_total_cost(self, obj):
        return self._calculate_costs_once(obj)[0]
        
    def get_material_cost(self, obj):
        return self._calculate_costs_once(obj)[1]

    def get_mo_cost(self, obj):
       return self._calculate_costs_once(obj)[2]




class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = '__all__'



class CostHistorySerializer(serializers.ModelSerializer):

    insumo_data = InsumoSerializer(source='insumo', read_only=True)

    class Meta:
        model = CostHistory
        fields = ('month_year', 'cost', 'cost_type', 'insumo_data')

