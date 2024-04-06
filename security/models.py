from crequest.middleware import CrequestMiddleware
from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal
import uuid

def get_user():
    current_request = CrequestMiddleware.get_request()
    result = None
    if current_request is not None:
        result = None if not current_request.user.is_authenticated else current_request.user

class Updater(models.Model):
    is_active  = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    created_by = models.CharField(max_length=500, null=True, blank=True, default=None, verbose_name="Creado por")
    updated_by = models.CharField(max_length=500, null=True, blank=True, default=None, verbose_name="Actualizado por")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_user()
        if user is not None:
            if not hasattr( self, 'created_by') or  self.created_by is None:
                self.created_by = user.username
            self.updated_by = user.username
        super(Updater, self).save(*args, **kwargs)

class Client(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    document_number = models.CharField(max_length=15,default=None, blank=True, null=True, verbose_name="Numero de documento")
    first_name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Primer nombre")
    second_name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Segundo nombre")
    last_name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Primer apellido")
    second_last_name = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Segundo apellido")
    email = models.EmailField(max_length=100,default=None, blank=True, null=True, verbose_name="Correo electronico")
    password = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="Contraseña")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client", blank=True, null=True, verbose_name="Usuario")

    def __str__(self):
        return "{}: {}".format(self.last_name, self.document_number)

    def complete_name(self):
        return f"{(self.last_name.upper())} {(self.second_last_name).upper()}, {(self.first_name).upper()}{' ' + (self.second_name).upper() if self.second_name else ''}"
    
    class Meta:
        db_table            = "client"
        verbose_name        = "Cliente"
        verbose_name_plural = "Clientes"
