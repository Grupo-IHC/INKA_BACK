from django.urls import path
from . import views

urlpatterns = [
    path('', views.SaleGetPost.as_view(), name='crear_listar_ventas'),
    path('design', views.DesignGetPost.as_view(), name='subir_diseños'),
    path('shopping', views.shoppingGet.as_view(), name='listar_mis_compras'),
]