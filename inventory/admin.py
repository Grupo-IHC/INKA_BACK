from django.contrib import admin
from inventory.models import *
from security.admin import default_list_display
from security.admin import default_list_editable
from security.admin import default_list_filter
from security.admin import default_search_fields
from security.admin import default_readonly_fields
from security.admin import default_fields

# Register your models here.
@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display    = ('id','name') + default_list_display
    # list_editable   = default_list_editable
    list_filter     = ('name',) + default_list_filter
    search_fields   = ('name',) + default_search_fields
    readonly_fields = default_readonly_fields
    fieldsets = (
        ('Información Básica', {
            'fields': ('name',),
        }),
        default_fields
    )

@admin.register(Entrance)
class EntranceAdmin(admin.ModelAdmin):
    list_display    = ('id','provider', 'product', 'quantity', 'date') + default_list_display
    # list_editable   = default_list_editable
    list_filter     = ('provider', 'product', 'quantity', 'date') + default_list_filter
    search_fields   = ('provider', 'product', 'quantity', 'date') + default_search_fields
    readonly_fields = default_readonly_fields
    list_select_related = ('provider',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('provider', 'product', 'quantity', 'date'),
        }),
        default_fields
    )

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display    = ('id','product', 'quantity') + default_list_display
    # list_editable   = default_list_editable
    list_filter     = ('product', 'quantity') + default_list_filter
    search_fields   = ('product', 'quantity') + default_search_fields
    readonly_fields = default_readonly_fields
    list_select_related = ('product',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('product', 'quantity'),
        }),
        default_fields
   )