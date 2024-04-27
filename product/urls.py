from django.urls import path
from . import views

urlpatterns = [
    path('filter', views.productFilterName.as_view(), name='filtrar_productos_por_nombre'),
    
    path('', views.productGetPost.as_view(), name='crear_listar_productos'), 
    path('type', views.typeGetPost.as_view(), name='crear_listar_tipos'),

    path('<str:code>', views.productGetByName.as_view(), name='obtener_actualizar_eliminar_producto'),
    
]