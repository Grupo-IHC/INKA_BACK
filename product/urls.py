from django.urls import path
from . import views

urlpatterns = [
    path('', views.productGetPost.as_view(), name='crear_listar_productos'), 
    path('<str:product_id>/', views.productGetById.as_view(), name='obtener_actualizar_eliminar_producto'),
]