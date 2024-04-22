from django.urls import path
from . import views

urlpatterns = [
    path('', views.saleGetPost.as_view(), name='crear_listar_ventas'),
]