from django.contrib import admin
from .models import State, Insumo, Composition, CompositionInsumo, CompositionComposition, CostHistory

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
    list_display = ['codigo', 'name', 'unit']


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'name', 'unit']
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
