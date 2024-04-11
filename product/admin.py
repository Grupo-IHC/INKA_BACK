from django.contrib import admin
from product.models import *
from security.admin import default_list_display
from security.admin import default_list_editable
from security.admin import default_list_filter
from security.admin import default_search_fields
from security.admin import default_readonly_fields
from security.admin import default_fields

# Register your models here.

@admin.register(CategoryProduct)
class CategoryProductAdmin(admin.ModelAdmin):
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

@admin.register(TypeProduct)
class TypeProductAdmin(admin.ModelAdmin):
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

@admin.register(ColorProduct)
class ColorProductAdmin(admin.ModelAdmin):
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

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display    = ('id','name', 'description',  'type_product', 'category_product','color_product', 'price', 'measure', 'image') + default_list_display
    # list_editable   = default_list_editable
    list_filter     = ('name', 'description',  'type_product', 'category_product', 'color_product', 'price', 'measure', 'image') + default_list_filter
    search_fields   = ('name', 'description',  'type_product', 'category_product', 'color_product', 'price', 'measure', 'image') + default_search_fields
    readonly_fields = default_readonly_fields
    list_select_related = ( 'type_product','color_product', 'category_product')
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'description',  'type_product', 'category_product', 'color_product', 'price', 'measure', 'image'),
        }),
        default_fields
    )