from rest_framework import serializers
from restaurantApp.models import restaurantModel, restFoodModel, restMenuModel
from frontend.models import OrderItem, Address, CartItem,Cart
from accounts.models import UserProfile
from accounts.serializers import UserDetailSerializer

class RestaurantSerializer(serializers.ModelSerializer):
    root_usr = serializers.SerializerMethodField()
    class Meta:
        model = restaurantModel
    #     fields = ('id','root_usr','rest_name','rest_owner_name','rest_phone','rest_address','rest_area','slug',
    #     'rest_city','rest_country','rest_opentime','rest_closetime','rest_image',
    #     'status','rest_description')
    # def get_root_usr(self,obj):
    #     return str(obj.root_usr.user_name)
        fields ='__all__'
    # def get_root_usr(self,obj):
    #     return UserDetailSerializer(obj.root_usr).data
    def get_root_usr(self,obj):
        return str(obj.root_usr.user_name)
class MenuSerializer(serializers.ModelSerializer):
    restaurant = serializers.SerializerMethodField()
    class Meta:
        model = restMenuModel
        fields = ('id','restaurant','Menu','special')

    def get_restaurant(self,obj):
        return str(obj.restaurant.rest_name)

class FoodSerializer(serializers.ModelSerializer):
    restaurant = serializers.SerializerMethodField()
    Menu = serializers.SerializerMethodField()
    class Meta:
        model = restFoodModel
        fields = '__all__'
    def get_restaurant(self,obj):
        return str(obj.restaurant.rest_name)
    def get_Menu(self,obj):
        return str(obj.Menu.Menu)
        
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
