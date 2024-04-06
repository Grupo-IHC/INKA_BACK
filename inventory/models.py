from django.db import models
from security.models import Updater
from django.contrib.auth.models import User
from django.utils import timezone
from product.models import Product
import uuid

class Provider(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Nombre")

    def __str__(self):
        return "{}".format(self.name)
    
    class Meta:
        db_table            = "provider"
        verbose_name        = "Proveedor"
        verbose_name_plural = "Proveedores"

class Entrance(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="entrances", verbose_name="Proveedor", default=None, blank=True, null=True,)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto",  default=None, blank=True, null=True)
    quantity = models.IntegerField(default=None, blank=True, null=True, verbose_name="Cantidad",)
    date = models.DateTimeField(default=timezone.now, verbose_name="Fecha",)

    def __str__(self):
        return "{} - {}".format(self.provider, self.date)
    
    class Meta:
        db_table            = "entrance"
        verbose_name        = "Entrada"
        verbose_name_plural = "Entradas"

class Inventory(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto", default=None, blank=True, null=True)
    quantity = models.IntegerField(default=None, blank=True, null=True, verbose_name="Cantidad",)

    def __str__(self):
        return "{} - {}".format(self.product, self.quantity)
    
    class Meta:
        db_table            = "inventory"
        verbose_name        = "Inventario"
        verbose_name_plural = "Inventarios"