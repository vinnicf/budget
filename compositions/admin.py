from django.contrib import admin
from .models import State, Insumo, Composition, CompositionInsumo, CompositionComposition, CostHistory, Classe, Grupo

# Inlines


class CompositionInsumoInline(admin.TabularInline):
    model = CompositionInsumo
    extra = 1


class CompositionCompositionInline(admin.TabularInline):
    model = CompositionComposition
    fk_name = "parent_composition"
    extra = 1

# ModelAdmin


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'name', 'unit','currentcost','insumo_type']


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'name', 'unit', 'comp_cost']
    inlines = [CompositionInsumoInline, CompositionCompositionInline]
    search_fields = ['codigo']


@admin.register(CompositionInsumo)
class CompositionInsumoAdmin(admin.ModelAdmin):
    list_display = ['insumo', 'composition', 'quantity']


@admin.register(CompositionComposition)
class CompositionCompositionAdmin(admin.ModelAdmin):
    list_display = ['parent_composition', 'child_composition', 'quantity']


@admin.register(CostHistory)
class CostHistoryAdmin(admin.ModelAdmin):
    list_display = ['insumo', 'state', 'month_year', 'cost']
    # Filtering by state and month_year can be helpful
    list_filter = ['state', 'month_year']


# Define the admin class for Classe
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

    

# Define the admin class for Grupo
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('name', 'classe')
    search_fields = ('name', 'classe__name', 'classe__code')
    list_filter = ('classe',)



# Register the models with their respective admin classes
admin.site.register(Classe, ClasseAdmin)
admin.site.register(Grupo, GrupoAdmin)