from django.db import models
from security.models import Updater
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Client(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    document_number = models.CharField(max_length=15,default=None, blank=True, null=True, verbose_name="Numero de documento")
    first_name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Primer nombre")
    second_name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Segundo nombre")
    last_name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Primer apellido")
    second_last_name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Segundo apellido")
    email = models.EmailField(max_length=100,default=None, blank=True, null=True, verbose_name="Correo electronico")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client", blank=True, null=True, verbose_name="Usuario")

    def __str__(self):
        return "{}: {}".format(self.last_name, self.document_number)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.user:

            username = self.document_number 
            password = f'{self.document_number}'
            email = self.email if self.email else None

            user = User.objects.create_user(username=username, password=password, email=email)

            self.user = user
            self.save() 

    def complete_name(self):
        return f"{(self.last_name.upper())} {(self.second_last_name).upper()}, {(self.first_name).upper()}{' ' + (self.second_name).upper() if self.second_name else ''}"
    
    class Meta:
        db_table            = "client"
        verbose_name        = "Cliente"
        verbose_name_plural = "Clientes"

class TypeStamp(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Nombre")

    def __str__(self):
        return "{} - {}".format(self.name)
    
    class Meta:
        db_table            = "type_stamp"
        verbose_name        = "Tipo de sello"
        verbose_name_plural = "Tipos de sello"

class Design(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Nombre")
    image = models.FileField(upload_to="designs/", default=None, blank=True, null=True, verbose_name="Imagen")

    def __str__(self):
        return "{} - {}".format(self.name, self.image)
    
    class Meta:
        db_table            = "design"
        verbose_name        = "Diseño"
        verbose_name_plural = "Diseños"

class CategoryStamp(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Nombre")

    def __str__(self):
        return "{}".format(self.name)
    
    class Meta:
        db_table            = "category_stamp"
        verbose_name        = "Categoria de sello"
        verbose_name_plural = "Categorias de sello"

class Stamp(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    type_stamp = models.ForeignKey(TypeStamp, on_delete=models.CASCADE, related_name="stamps", verbose_name="Tipo de sello")
    category_stamp = models.ForeignKey(CategoryStamp, on_delete=models.CASCADE, related_name="stamps", verbose_name="Categoria de sello")
    design = models.ForeignKey(Design, on_delete=models.CASCADE, related_name="stamps", verbose_name="Diseño")
    name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Nombre")
    code = models.CharField(max_length=20, default=None, blank=True, null=True, verbose_name="Codigo")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Precio")
    description = models.TextField(default=None, blank=True, null=True, verbose_name="Descripcion")

    def __str__(self):
        return "{}".format(self.type_stamp.name)
    
    class Meta:
        db_table            = "stamp"
        verbose_name        = "Sello"
        verbose_name_plural = "Sellos"

class ColorStamp(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Nombre")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Precio")

    def __str__(self):
        return "{} - {}".format(self.name, self.price)
    
    class Meta:
        db_table            = "color_stamp"
        verbose_name        = "Color de sello"
        verbose_name_plural = "Colores de sello"

class Cartridge(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Nombre")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Precio")

    def __str__(self):
        return "{} - {}".format(self.name, self.price)
    
    class Meta:
        db_table            = "cartridge"
        verbose_name        = "Cartucho"
        verbose_name_plural = "Cartuchos"

class Order(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="orders", verbose_name="Cliente", default=None, blank=True, null=True,)
    stamp = models.ForeignKey(Stamp, on_delete=models.CASCADE, related_name="orders", verbose_name="Sello", default=None, blank=True, null=True,)
    color_stamp = models.ForeignKey(ColorStamp, on_delete=models.CASCADE, related_name="orders", verbose_name="Color de sello", default=None, blank=True, null=True,)
    cartridge = models.ForeignKey(Cartridge, on_delete=models.CASCADE, related_name="orders", verbose_name="Cartucho", default=None, blank=True, null=True,)
    quantity = models.IntegerField(default=1, verbose_name="Cantidad", blank=True, null=True,)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total", blank=True, null=True,)

    def __str__(self):
        return "{} - {}: {}".format(self.client.complete_name(), self.stamp.design.name)
    
    class Meta:
        db_table            = "order"
        verbose_name        = "Orden"
        verbose_name_plural = "Ordenes"

class PayMode(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Nombre")

    def __str__(self):
        return "{}".format(self.name)
    
    class Meta:
        db_table            = "pay_mode"
        verbose_name        = "Modo de pago"
        verbose_name_plural = "Modos de pago"

class ShoppingCar(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    order = models.ManyToManyField(Order, related_name="shopping_cars", verbose_name="Orden", default=None, blank=True)
    pay_mode = models.ForeignKey(PayMode, on_delete=models.CASCADE, verbose_name="Modo de pago", default=None, blank=True, null=True,)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total", blank=True, null=True,)

    def __str__(self):
        return "{}: {}".format(self.id, self.total)
    
    class Meta:
        db_table            = "shopping_car"
        verbose_name        = "Carrito de compras"
        verbose_name_plural = "Carritos de compras"
