# Generated by Django 5.1.4 on 2025-07-24 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_cart_added_at_remove_product_review_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='qr_code_image',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/'),
        ),
    ]
