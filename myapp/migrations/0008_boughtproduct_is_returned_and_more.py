# Generated by Django 5.1.4 on 2025-07-25 00:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_returnproduct_delete_return'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='boughtproduct',
            name='is_returned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='boughtproduct',
            name='payment_method',
            field=models.CharField(choices=[('UPI', 'UPI'), ('Card', 'Card')], default='Card', max_length=10),
        ),
        migrations.AddField(
            model_name='boughtproduct',
            name='price_per_item',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='boughtproduct',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='boughtproduct',
            name='return_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.returnproduct'),
        ),
        migrations.AddField(
            model_name='boughtproduct',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sold_products', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='boughtproduct',
            name='shipping_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='boughtproduct',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
