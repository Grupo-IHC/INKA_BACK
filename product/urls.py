from django.urls import path
from . import views

urlpatterns = [
    path('', views.productGetPost.as_view(), name='crear_listar_productos'), 
    path('type', views.typeGetPost.as_view(), name='crear_listar_tipos'),
    # path('category', views.categoryGetPost.as_view(), name='crear_listar_categorias'),

    path('<str:product_id>', views.productGetById.as_view(), name='obtener_actualizar_eliminar_producto'),
    # path('category/<str:category_id>', views.categoryGetById.as_view(), name='obtener_actualizar_eliminar_categoria'),
    # path('type/<str:type_id>', views.typeGetById.as_view(), name='obtener_actualizar_eliminar_tipo'),
]