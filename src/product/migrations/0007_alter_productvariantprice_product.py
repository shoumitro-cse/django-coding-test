# Generated by Django 4.0 on 2021-12-16 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_product_created_product_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariantprice',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_variant_prices', to='product.product'),
        ),
    ]
