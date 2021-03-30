from django.contrib import admin
from frontend.models import OrderItem, Address, Payment,Cart,CartItem,Order
# Register your models here.
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)