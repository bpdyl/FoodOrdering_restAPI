from rest_framework import serializers
from .models import *
from foodBackend.serializers import *

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    food = FoodSerializer()
    cart = CartSerializer()
    class Meta:
        model = CartItem
        fields = '_all_'


class OrderSerializer(serializers.ModelSerializer):
    # order_item = OrderItem
    class Meta:
        model = Order
        fields = '__all__'    

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id','amount','timestamp')