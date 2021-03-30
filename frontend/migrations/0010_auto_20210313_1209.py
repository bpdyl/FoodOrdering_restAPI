# Generated by Django 3.1.7 on 2021-03-13 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantApp', '0004_auto_20210313_0740'),
        ('frontend', '0009_auto_20210313_0815'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='order',
            old_name='ordered_date',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.cart'),
        ),
        migrations.AddField(
            model_name='order',
            name='restaurants',
            field=models.ManyToManyField(related_name='orders', to='restaurantApp.restaurantModel'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='frontend.order'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='restaurantApp.restaurantmodel'),
        ),
    ]
