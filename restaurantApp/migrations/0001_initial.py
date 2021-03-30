# Generated by Django 3.1.7 on 2021-03-08 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='restaurantModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rest_name', models.CharField(max_length=1000)),
                ('rest_owner_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('rest_phone', models.IntegerField(blank=True, null=True)),
                ('rest_address', models.CharField(blank=True, max_length=10000, null=True)),
                ('rest_area', models.CharField(blank=True, max_length=1000, null=True)),
                ('slug', models.SlugField(max_length=250, unique_for_date='rest_reg_date')),
                ('rest_city', models.CharField(blank=True, max_length=1000, null=True)),
                ('rest_country', models.CharField(blank=True, max_length=1000, null=True)),
                ('rest_opentime', models.TimeField(blank=True, null=True)),
                ('rest_closetime', models.TimeField(blank=True, null=True)),
                ('rest_image', models.ImageField(blank=True, max_length=10000, null=True, upload_to='')),
                ('rest_reg_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('closed', 'Close'), ('open', 'Open')], default='open', max_length=10)),
                ('rest_description', models.CharField(blank=True, max_length=10000, null=True)),
                ('rest_merchant_id', models.IntegerField(blank=True, null=True)),
                ('root_usr', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restaurants', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('rest_reg_date',),
            },
        ),
        migrations.CreateModel(
            name='restMenuModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Menu', models.CharField(max_length=3000)),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurantApp.restaurantmodel')),
            ],
        ),
        migrations.CreateModel(
            name='restFoodModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(db_index=False, null=True)),
                ('food_name', models.CharField(max_length=3000)),
                ('food_image', models.ImageField(blank=True, max_length=5000, null=True, upload_to='')),
                ('food_description', models.CharField(blank=True, max_length=10000, null=True)),
                ('food_price', models.PositiveIntegerField()),
                ('Menu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurantApp.restmenumodel')),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurantApp.restaurantmodel')),
            ],
            options={
                'unique_together': {('slug', 'Menu', 'restaurant')},
            },
        ),
    ]