from django.contrib import admin
from django.contrib.auth.models import Group
from security.models import *
# from .models import UserProfile

default_list_display    = ('is_active', 'created_at', 'created_by', 'updated_at', 'updated_by')
default_list_editable   = ('is_active',)
default_list_filter     = ('created_at', 'created_by', 'updated_at', 'updated_by')
default_search_fields   = ('created_at', 'created_by', 'updated_at', 'updated_by')
default_readonly_fields = ('created_at', 'created_by', 'updated_at', 'updated_by')
default_fields          = ('Información de Auditoria', {
                            'fields': (
                                ('created_at', 'created_by'),
                                ('updated_at', 'updated_by')
                            )
                        })

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display    = ('id','document_number', 'first_name', 'second_name', 'last_name', 'second_last_name', 'email', 'user') + default_list_display
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
