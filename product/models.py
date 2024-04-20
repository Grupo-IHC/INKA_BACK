from django.db import models
from security.models import Updater
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# Create your models here.
class CategoryProduct(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Nombre")
    description = models.TextField(default=None, blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return "{}".format(self.name)
    
    class Meta:
        db_table            = "category_product"
        verbose_name        = "Categoría de producto"
        verbose_name_plural = "Categorías de productos"

class TypeProduct(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Nombre")
    description = models.TextField(default=None, blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return "{}".format(self.name)
    
    class Meta:
        db_table            = "type_product"
        verbose_name        = "Tipo de producto"
        verbose_name_plural = "Tipos de productos"

class ColorProduct(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Nombre")
    description = models.TextField(default=None, blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return "{}".format(self.name)
    
    class Meta:
        db_table            = "color_product"
        verbose_name        = "Color de producto"
        verbose_name_plural = "Colores de productos"

class Product(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    code = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Código")
    name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Nombre")
    description = models.TextField(default=None, blank=True, null=True, verbose_name="Descripción")
    type_product = models.ForeignKey(TypeProduct, on_delete=models.CASCADE, related_name="products", verbose_name="Tipo de producto",default=None, blank=True, null=True)
    color_product = models.ForeignKey(ColorProduct, on_delete=models.CASCADE, related_name="products", verbose_name="Color de producto",default=None, blank=True, null=True)
    category_product = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, related_name="products", verbose_name="Categoría",default=None, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True, verbose_name="Precio")
    measure = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Medida")
    image = models.FileField(upload_to="products/", default=None, blank=True, null=True, verbose_name="Imagen")

    def __str__(self):
        return "{} - {}".format(self.name, self.price)
    
    class Meta:
        db_table            = "product"
        verbose_name        = "Producto"
        verbose_name_plural = "Productos"