# Generated by Django 3.1.7 on 2021-03-12 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0004_auto_20210312_1719'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='price',
            new_name='food_price',
        ),
    ]