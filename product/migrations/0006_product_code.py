# Generated by Django 5.0.3 on 2024-04-20 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_remove_typeproduct_category_product_category_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='code',
            field=models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Código'),
        ),
    ]