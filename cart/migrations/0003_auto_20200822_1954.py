# Generated by Django 2.2.15 on 2020-08-22 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20200822_0011'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='pincode',
            new_name='zipcode',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='shipping_address',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.Order'),
        ),
    ]
