
# Create your views here.
from rest_framework import generics,viewsets, filters, permissions
from rest_framework.views import APIView
from restaurantApp.models import restaurantModel,restMenuModel,restFoodModel
from .serializers import RestaurantSerializer,MenuSerializer,FoodSerializer,AddressSerializer
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAdminUser, DjangoModelPermissions, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

class RestaurantUserUpdatePermission(BasePermission):
    message = 'Editing option is available to seller only.'

    def has_object_permission(self,request,view,obj):
        
        if request.method in SAFE_METHODS:
            return True
        return obj.root_usr == request.user

# class RestaurantList(viewsets.ModelViewSet):
#     permission_classes = [RestaurantUserUpdatePermission]
#     serializer_class = RestaurantSerializer
    
#     def get_object(self, queryset = None, **kwargs):
#         item = self.kwargs.get('pk')
#         return get_object_or_404(restaurantModel, slug = item)
        
#     #define custom Queryset
#     def get_queryset(self):
#         return restaurantModel.objects.all()


# class RestaurantList(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = restaurantModel.restobjects.all()

#     def list(self, request):
#         serializer_class = RestaurantSerializer(self.queryset, many = True)
#         return Response(serializer_class.data)
    
#     def retrieve(self, request, pk=None):
#         restaurant = get_object_or_404(self.queryset, pk = pk)
#         serializer_class = RestaurantSerializer(restaurant)
#         return Response(serializer_class.data)
class RestaurantList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = restaurantModel.restobjects.all()
    serializer_class = RestaurantSerializer

class RestaurantDetail(generics.RetrieveAPIView):
    serializer_class = RestaurantSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(restaurantModel, slug=item)
   
class RestaurantDetailfilter(generics.ListAPIView):
    queryset = restaurantModel.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^slug','^rest_area','foods__food_name']


# class CreateRestaurant(generics.CreateAPIView):
#     permission_classes = [permissions.IsAuthenticated, RestaurantUserUpdatePermission]
#     queryset = restaurantModel.objects.all()
#     serializer_class = RestaurantSerializer

class AdminRestaurantCreate(APIView):
    permission_classes = [IsAuthenticated,RestaurantUserUpdatePermission]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        print(request.data)
        serializer = restaurantModel(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class AdminRestaurantDetail(generics.RetrieveAPIView):
    permission_classes = [RestaurantUserUpdatePermission]
    queryset = restaurantModel.objects.all()
    serializer_class = RestaurantSerializer


class EditRestaurant(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, RestaurantUserUpdatePermission]
    serializer_class = RestaurantSerializer
    queryset = restaurantModel.objects.all()

class DeleteRestaurant(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, RestaurantUserUpdatePermission]
    serializer_class = RestaurantSerializer
    queryset = restaurantModel.objects.all()

class MenuList(generics.ListCreateAPIView):
    queryset = restMenuModel.objects.all()
    serializer_class = MenuSerializer

class AdminMenuDetail(generics.RetrieveAPIView):
    permission_classes = [RestaurantUserUpdatePermission]
    queryset = restMenuModel.objects.all()
    serializer_class = MenuSerializer
class EditMenu(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, RestaurantUserUpdatePermission]
    serializer_class = MenuSerializer
    queryset = restMenuModel.objects.all()

class DeleteMenu(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, RestaurantUserUpdatePermission]
    serializer_class = RestaurantSerializer
    queryset = restaurantModel.objects.all()

class FoodList(generics.ListCreateAPIView):
    queryset = restFoodModel.objects.all()
    serializer_class = FoodSerializer


