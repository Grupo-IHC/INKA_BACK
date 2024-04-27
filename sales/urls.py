from django.urls import path
from . import views

urlpatterns = [
    path('', views.SaleGetPost.as_view(), name='crear_listar_ventas'),
    path('shopping', views.shoppingGet.as_view(), name='listar_mis_compras'),
]