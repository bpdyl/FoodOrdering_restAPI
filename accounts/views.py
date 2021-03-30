from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import RegisterUserSerializer, UserDetailSerializer
from .models import NewUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class CustomUserCreate(APIView):
    permisssion_classes = [AllowAny]

    def post(self, request):
        reg_serializer = RegisterUserSerializer(data = request.data)
        if reg_serializer.is_valid():
            newuser = reg_serializer.save()
            if newuser:
                return Response(status = status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class BlackListTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = NewUser.objects.all()
    serializer_class = UserDetailSerializer
