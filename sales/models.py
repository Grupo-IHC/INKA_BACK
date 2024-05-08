from django.db import models
from security.models import *
from django.contrib.auth.models import User
from django.utils import timezone
from product.models import *
import uuid

# Create your models here.

class Order(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    # client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="orders", verbose_name="Cliente", default=None, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto", default=None, blank=True, null=True)
    desing = models.CharField(default=None, blank=True, null=True, verbose_name="Diseño")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True, verbose_name="Precio")
    quantity = models.IntegerField(default=None, blank=True, null=True, verbose_name="Cantidad")

    def __str__(self):
        return "{}".format(self.product)
    
    class Meta:
        db_table            = "order"
        verbose_name        = "Orden"
        verbose_name_plural = "Ordenes"

class MethodPayment(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Nombre")
    description = models.TextField(default=None, blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return "{}".format(self.name)
    
    class Meta:
        db_table            = "method_payment"
        verbose_name        = "Metodo de pago"
        verbose_name_plural = "Metodos de pago"

class TypeDelivery(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Nombre")
    description = models.TextField(default=None, blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return "{}".format(self.name)
    
    class Meta:
        db_table            = "type_delivery"
        verbose_name        = "Tipo de entrega"
        verbose_name_plural = "Tipos de entrega"

class Pedido(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    order = models.ManyToManyField(Order, related_name="details", verbose_name="Orden", default=None, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="orders_clients", verbose_name="Cliente", default=None, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True, verbose_name="Precio")
    address = models.CharField(default=None, blank=True, null=True, verbose_name="Dirección")
    contact = models.CharField(default=None, blank=True, null=True, verbose_name="Contacto")
    contact_dni = models.CharField(default=None, blank=True, null=True, verbose_name="Contacto DNI")
    quantity = models.IntegerField(default=None, blank=True, null=True, verbose_name="Cantidad")
    date = models.DateTimeField(default=timezone.now, verbose_name="Fecha", blank=True, null=True)
    type_delivery = models.ForeignKey(TypeDelivery, on_delete=models.CASCADE, related_name="orders_details", verbose_name="Tipo de entrega", default=None, blank=True, null=True)
    method_payment = models.ForeignKey(MethodPayment, on_delete=models.CASCADE, related_name="orders_details", verbose_name="Metodo de pago", default=None, blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.date)
    
    class Meta:
        db_table            = "order_detail"
        verbose_name        = "Detalle de orden"
        verbose_name_plural = "Detalles de ordenes"