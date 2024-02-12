from django.contrib import admin
from .models import Orcamento, OrcamentoItem

class OrcamentoItemInline(admin.TabularInline):
    model = OrcamentoItem
    extra = 0 #No extra forms
    can_delete = False
    readonly_fields = ('refid', 'itemtype', 'subtype', 'codigo', 'description', 'unit', 'quantity', 'unit_cost', 'mo_cost', 'material_cost')  # Make fields read-only

    def has_add_permission(self, request, obj=None):
        return False




@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_email', 'created_at', 'desonerado', 'state', 'items_count')
    search_fields = ('name', 'state')
    list_filter = ('desonerado', 'state')
    inlines = [OrcamentoItemInline]  # Add this line

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'  # Column header


    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = 'Items Count'  # Column header

@admin.register(OrcamentoItem)
class OrcamentoItemAdmin(admin.ModelAdmin):
    list_display = ('orcamento', 'description', 'quantity', 'unit_cost')
    search_fields = ('description',)
