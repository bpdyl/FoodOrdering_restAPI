# Generated by Django 3.1.7 on 2021-03-13 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0005_auto_20210312_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(blank=True, choices=[('Order Received', 'Order Received'), ('Order Processing', ' Order Processing'), ('On the way', 'On the way'), ('Order Delivered', 'Order Delivered'), ('Order Cancelled', 'Order Cancelled')], max_length=50, null=True),
        ),
    ]
