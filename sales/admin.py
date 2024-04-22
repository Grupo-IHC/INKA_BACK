from django.contrib import admin
from sales.models import *
from security.admin import default_list_display
from security.admin import default_list_editable
from security.admin import default_list_filter
from security.admin import default_search_fields
from security.admin import default_readonly_fields
from security.admin import default_fields
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display    = ('id', 'product', 'desing', 'price', 'quantity') + default_list_display
    # list_editable   = default_list_editable
    list_filter     = default_list_filter
    search_fields   = ('product',) + default_search_fields
    readonly_fields = default_readonly_fields
    list_select_related = ( 'product',)
    fieldsets = (
        ('Información Básica', {
            'fields': ( 'product', 'desing', 'price', 'quantity'),
        }),
        default_fields
    )

@admin.register(MethodPayment)
class MethodPaymentAdmin(admin.ModelAdmin):
    list_display    = ('id','name', 'description') + default_list_display
    # list_editable   = default_list_editable
    list_filter     = ('name', 'description') + default_list_filter
    search_fields   = ('name', 'description') + default_search_fields
    readonly_fields = default_readonly_fields
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'description'),
        }),
        default_fields
    )

@admin.register(TypeDelivery)
class TypeDeliveryAdmin(admin.ModelAdmin):
    list_display    = ('id','name', 'description') + default_list_display
    # list_editable   = default_list_editable
    list_filter     = ('name', 'description') + default_list_filter
    search_fields   = ('name', 'description') + default_search_fields
    readonly_fields = default_readonly_fields
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'description'),
        }),
        default_fields
    )

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display    = ('id', 'client', 'price', 'address', 'contact', 'contact_dni', 'quantity', 'date','type_delivery', 'method_payment') + default_list_display
    # list_editable   = default_list_editable
    list_filter     = ('order', 'client', 'price', 'address', 'contact', 'contact_dni', 'quantity', 'date') + default_list_filter
    search_fields   = ('order', 'client', 'price', 'address', 'contact', 'contact_dni', 'quantity', 'date') + default_search_fields
    readonly_fields = default_readonly_fields
    list_select_related = ('client', 'order','type_delivery', 'method_payment')
    fieldsets = (
        ('Información Básica', {
            'fields': ('order', 'client', 'price', 'address', 'contact', 'contact_dni', 'quantity', 'date','type_delivery', 'method_payment'),
        }),
        default_fields
    )