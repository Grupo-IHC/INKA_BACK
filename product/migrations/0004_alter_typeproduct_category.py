# Generated by Django 5.0.3 on 2024-04-09 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_remove_typeproduct_category_typeproduct_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeproduct',
            name='category',
            field=models.ManyToManyField(blank=True, default=None, related_name='types', to='product.categoryproduct', verbose_name='Categoría'),
        ),
    ]