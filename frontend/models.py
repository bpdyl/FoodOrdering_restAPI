from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.db.models.signals import post_save,pre_save
from restaurantApp.models import restFoodModel,restaurantModel
from django.dispatch import receiver

# Create your models here.

ADDRESS_CHOICES = (
    ('B', 'Billing Address'),
    ('S', 'Shipping Address')
)
ORDER_STATUS = (
    ("Order Received","Order Received"),
    ("Order Processing"," Order Processing"),
    ("On the way", "On the way"),
    ("Order Delivered","Order Delivered"),
    ("Order Cancelled","Order Cancelled"),
)

class Cart(models.Model):
    user =models.OneToOneField(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    ordered = models.BooleanField(default = False)
    total_price = models.PositiveIntegerField(default = 0)
    
    def __str__(self):
        return str(self.user.user_name) + " " + str(self.total_price)

class CartItem(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    food_item = models.ForeignKey(restFoodModel,on_delete=models.CASCADE)
    # restaurants = models.OneToOneField(restaurantModel,on_delete=models.CASCADE)
    cart_restaurant = models.CharField(max_length=100, null = True, blank =True)
    food_price = models.PositiveIntegerField(default = 0)
    isOrder = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default = 1)

    class Meta:
        ordering = ['user','-created_at']
    
    def __str__(self):
        return str(self.user.user_name) + " " + str(self.food_item.food_name)

@receiver(pre_save, sender=CartItem)
def correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_food = restFoodModel.objects.get(id=cart_items.food_item.id)
    restaurant_reference = restFoodModel.objects.get(id = cart_items.food_item.id)
    cart_items.cart_restaurant = restaurant_reference.restaurant
    cart_items.food_price = cart_items.quantity * price_of_food.food_price
    # total_cart_items = CartItem.objects.filter(user = cart_items.user)
    # cart = Cart.objects.get(id = cart_items.cart.id)    
    # cart.total_price = cart_items.price
    # cart.save()    


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, null =True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True )
    billing_address = models.ForeignKey('Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True )
    order_status = models.CharField(max_length=50, choices = ORDER_STATUS, null =True,blank = True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    restaurants = models.ManyToManyField(restaurantModel, related_name='orders')
    created_at = models.DateTimeField(auto_now_add = True,blank = True,null = True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.user.user_name

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name = 'items', on_delete=models.CASCADE,null = True)
    food_item = models.ForeignKey(restFoodModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    ordered = models.BooleanField(default=False)
    restaurant = models.ForeignKey(restaurantModel,related_name='items',on_delete=models.CASCADE,null = True)
    is_paid = models.BooleanField(default = False)
    def __str__(self):
        return self.user.user_name


    def __str__(self):
        return f"{self.quantity} of {self.food_item.food_name}"

    def get_total_item_price(self):
        return self.quantity * self.price




class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100,default = "None")
    zip_code = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.user_name

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.IntegerField()
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.user_name
