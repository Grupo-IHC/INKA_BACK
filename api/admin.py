from django.contrib import admin
from api.models import *
from security.admin import default_list_display
from security.admin import default_list_editable
from security.admin import default_list_filter
from security.admin import default_search_fields
from security.admin import default_readonly_fields
from security.admin import default_fields

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display    = ('document_number', 'first_name', 'second_name', 'last_name', 'second_last_name', 'email', 'user') + default_list_display
    # list_editable   = default_list_editable
    list_filter     = ('document_number', 'first_name', 'second_name', 'last_name', 'second_last_name', 'email') + default_list_filter
    search_fields   =  ('document_number', 'first_name', 'second_name', 'last_name', 'second_last_name', 'email') + default_search_fields
    readonly_fields = default_readonly_fields
    list_select_related = ('user',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('document_number', 'first_name', 'second_name', 'last_name', 'second_last_name', 'email', 'user'),
        }),
        default_fields
    )

@admin.register(TypeStamp)
class TypeStampAdmin(admin.ModelAdmin):
    list_display    = ('name',) + default_list_display
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

@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display    = ('name', 'image') + default_list_display
    # list_editable   = default_list_editable
    list_filter     = ('name', 'image') + default_list_filter
    search_fields   = ('name', 'image') + default_search_fields
    readonly_fields = default_readonly_fields
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'image'),
        }),
        default_fields
    )

@admin.register(Stamp)
class StampAdmin(admin.ModelAdmin):
    list_display    = ('type_stamp', 'category_stamp', 'design', 'name', 'code', 'price', 'description') + default_list_display
    # list_editable   = default_list_editable
    list_filter     = ('type_stamp', 'category_stamp') + default_list_filter
    search_fields   = ('name', 'code', 'description') + default_search_fields
    readonly_fields = default_readonly_fields
    fieldsets = (
        ('Información Básica', {
            'fields': ('type_stamp', 'category_stamp', 'design', 'name', 'code', 'price', 'description'),
        }),
        default_fields
    )

@admin.register(CategoryStamp)
class CategoryStampAdmin(admin.ModelAdmin):
    list_display    = ('name',) + default_list_display
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

@admin.register(ColorStamp)
class ColorStampAdmin(admin.ModelAdmin):
    list_display    = ('name', 'price') + default_list_display
    # list_editable   = default_list_editable
    list_filter     = ('name', 'price') + default_list_filter
    search_fields   = ('name', 'price') + default_search_fields
    readonly_fields = default_readonly_fields
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'price'),
        }),
        default_fields
    )

@admin.register(Cartridge)
class CartridgeAdmin(admin.ModelAdmin):
    list_display    = ('name', 'price') + default_list_display
    # list_editable   = default_list_editable
    list_filter     = ('name', 'price') + default_list_filter
    search_fields   = ('name', 'price') + default_search_fields
    readonly_fields = default_readonly_fields
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'price'),
        }),
        default_fields
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display    = ('client', 'stamp', 'color_stamp', 'cartridge', 'quantity', 'total') + default_list_display
    # list_editable   = default_list_editable
    list_filter     = ('client', 'stamp', 'color_stamp', 'cartridge') + default_list_filter
    search_fields   = ('client', 'stamp', 'color_stamp', 'cartridge') + default_search_fields
    readonly_fields = default_readonly_fields
    fieldsets = (
        ('Información Básica', {
            'fields': ('client', 'stamp', 'color_stamp', 'cartridge', 'quantity', 'total'),
        }),
        default_fields
    )

@admin.register(PayMode)
class PayModeAdmin(admin.ModelAdmin):
    list_display    = ('name',) + default_list_display
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

@admin.register(ShoppingCar)
class ShoppingCarAdmin(admin.ModelAdmin):
    list_display    = ('id', 'total') + default_list_display
    # list_editable   = default_list_editable
    list_filter     = default_list_filter
    search_fields   = ('order', 'paymode') + default_search_fields
    readonly_fields = default_readonly_fields
    fieldsets = (
        ('Información Básica', {
            'fields': ('id','order', 'paymode','total'),
        }),
        default_fields
    )