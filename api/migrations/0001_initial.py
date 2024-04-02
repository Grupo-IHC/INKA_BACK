# Generated by Django 5.0.3 on 2024-03-29 18:44

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cartridge',
            fields=[
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('created_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Creado por')),
                ('updated_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Actualizado por')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Nombre')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Precio')),
            ],
            options={
                'verbose_name': 'Cartucho',
                'verbose_name_plural': 'Cartuchos',
                'db_table': 'cartridge',
            },
        ),
        migrations.CreateModel(
            name='CategoryStamp',
            fields=[
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('created_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Creado por')),
                ('updated_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Actualizado por')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Categoria de sello',
                'verbose_name_plural': 'Categorias de sello',
                'db_table': 'category_stamp',
            },
        ),
        migrations.CreateModel(
            name='ColorStamp',
            fields=[
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('created_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Creado por')),
                ('updated_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Actualizado por')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Nombre')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Precio')),
            ],
            options={
                'verbose_name': 'Color de sello',
                'verbose_name_plural': 'Colores de sello',
                'db_table': 'color_stamp',
            },
        ),
        migrations.CreateModel(
            name='Design',
            fields=[
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('created_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Creado por')),
                ('updated_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Actualizado por')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Nombre')),
                ('image', models.FileField(blank=True, default=None, null=True, upload_to='designs/', verbose_name='Imagen')),
            ],
            options={
                'verbose_name': 'Diseño',
                'verbose_name_plural': 'Diseños',
                'db_table': 'design',
            },
        ),
        migrations.CreateModel(
            name='PayMode',
            fields=[
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('created_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Creado por')),
                ('updated_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Actualizado por')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Modo de pago',
                'verbose_name_plural': 'Modos de pago',
                'db_table': 'pay_mode',
            },
        ),
        migrations.CreateModel(
            name='TypeStamp',
            fields=[
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('created_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Creado por')),
                ('updated_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Actualizado por')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Tipo de sello',
                'verbose_name_plural': 'Tipos de sello',
                'db_table': 'type_stamp',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('created_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Creado por')),
                ('updated_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Actualizado por')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_number', models.CharField(blank=True, default=None, max_length=15, null=True, verbose_name='Numero de documento')),
                ('first_name', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Primer nombre')),
                ('second_name', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Segundo nombre')),
                ('last_name', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Primer apellido')),
                ('second_last_name', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Segundo apellido')),
                ('email', models.EmailField(blank=True, default=None, max_length=100, null=True, verbose_name='Correo electronico')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'db_table': 'client',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('created_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Creado por')),
                ('updated_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Actualizado por')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=1, null=True, verbose_name='Cantidad')),
                ('total', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Total')),
                ('cartridge', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='api.cartridge', verbose_name='Cartucho')),
                ('client', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='api.client', verbose_name='Cliente')),
                ('color_stamp', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='api.colorstamp', verbose_name='Color de sello')),
            ],
            options={
                'verbose_name': 'Orden',
                'verbose_name_plural': 'Ordenes',
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCar',
            fields=[
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('created_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Creado por')),
                ('updated_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Actualizado por')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Total')),
                ('order', models.ManyToManyField(blank=True, default=None, related_name='shopping_cars', to='api.order', verbose_name='Orden')),
                ('pay_mode', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.paymode', verbose_name='Modo de pago')),
            ],
            options={
                'verbose_name': 'Carrito de compras',
                'verbose_name_plural': 'Carritos de compras',
                'db_table': 'shopping_car',
            },
        ),
        migrations.CreateModel(
            name='Stamp',
            fields=[
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('created_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Creado por')),
                ('updated_by', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Actualizado por')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Nombre')),
                ('code', models.CharField(blank=True, default=None, max_length=20, null=True, verbose_name='Codigo')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Precio')),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='Descripcion')),
                ('category_stamp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stamps', to='api.categorystamp', verbose_name='Categoria de sello')),
                ('design', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stamps', to='api.design', verbose_name='Diseño')),
                ('type_stamp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stamps', to='api.typestamp', verbose_name='Tipo de sello')),
            ],
            options={
                'verbose_name': 'Sello',
                'verbose_name_plural': 'Sellos',
                'db_table': 'stamp',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='stamp',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='api.stamp', verbose_name='Sello'),
        ),
    ]