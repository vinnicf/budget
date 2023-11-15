from django.contrib import admin
from .models import Orcamento, OrcamentoItem

@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'desonerado', 'state')  # Customize as needed
    search_fields = ('name', 'state')  # Customize as needed
    list_filter = ('desonerado', 'state')  # Customize as needed
    # You can add more options here to customize the admin interface

@admin.register(OrcamentoItem)
class OrcamentoItemAdmin(admin.ModelAdmin):
    list_display = ('orcamento', 'description', 'quantity', 'unit_cost')  # Customize as needed
    search_fields = ('description',)  # Customize as needed
    # You can add more options here to customize the admin interface
