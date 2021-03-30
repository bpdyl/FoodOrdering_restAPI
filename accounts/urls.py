from django.urls import path
from .views import CustomUserCreate,BlackListTokenView,UserDetail

app_name = 'accounts'

urlpatterns = [
    path('register/',CustomUserCreate.as_view(),name='create_user'),
    path('logout/blacklist/',BlackListTokenView.as_view(),name='blacklist'),
    path('profile/',UserDetail.as_view(),name='customer_profile'),
]