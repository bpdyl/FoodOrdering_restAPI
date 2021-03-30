
from django.views.generic import TemplateView
from .views import (RestaurantList,RestaurantDetail,RestaurantDetailfilter,
CreateRestaurant,EditRestaurant,AdminRestaurantDetail,
DeleteRestaurant)
# from rest_framework.routers import DefaultRouter
from django.urls import path

app_name = 'foodBackend'

# router = DefaultRouter()
# router.register('',RestaurantList, basename='restaurant')
# urlpatterns = router.urls

urlpatterns = [
    path('',RestaurantList.as_view(), name='restaurant_list'),
    path('restaurants/<str:pk>/', RestaurantDetail.as_view(), name='restaurant_detail'),
    path('search/', RestaurantDetailfilter.as_view(), name='search_restaurant'),
    path('admin/restaurant/create/',CreateRestaurant.as_view(),name='create_restaurant'),
    path('admin/restaurant/edit/restaurantdetail/<int:pk>/',AdminRestaurantDetail.as_view(),
    name='adminrestaurantdetail'),
    path('admin/restaurant/edit/<int:pk>',EditRestaurant.as_view(),name='edit_restaurant'),
    path('admin/restaurant/delete/<int:pk>/', DeleteRestaurant.as_view(),name='delete_restaurant'),
    
]