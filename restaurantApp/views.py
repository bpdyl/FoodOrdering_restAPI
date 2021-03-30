from django.shortcuts import render

# Create your views here.
from frontend.serializers import FoodSerializer,AddressSerializer,MenuSerializer,OrderSerializer

class AdminOrderView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    serializer_class = Add

