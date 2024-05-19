from django.urls import path
from . import views

urlpatterns = [

    #FILTRAR PRODUCTOS POR NOMBRE
    path('filter', views.productFilterName.as_view(), name='filtrar_productos_por_nombre'),
    
    #CREAR PRODUCTOS Y LISTAR TODOS LOS PRODUCTOS 
    path('', views.productGetPost.as_view(), name='crear_listar_productos'), 

    #LISTAR Y CREAR TIPOS DE PRODUCTOS
    path('type', views.typeGetPost.as_view(), name='crear_listar_tipos'),

    #OBTENER INFORMACIÓN DE UN PRODUCTO POR SU CÓDIGO
    path('<str:code>', views.productGetByCode.as_view(), name='obtener_actualizar_eliminar_producto'),
    
]