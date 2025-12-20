from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsAdminUser, IsOwnerOrAdmin
from .models import User
from .serializers import (
    UserSerializer,
    UserDetailSerializer,
    UserProfileSerializer,
    MyTokenObtainPairSerializer
)
# from .permissions import IsAdminUser, IsOwnerOrAdmin

from django.shortcuts import render

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Decide permissions based on action
        """
    
        if self.action in ['list','create']:
            return [IsAdminUser()]
        else:
            return [IsOwnerOrAdmin()]

    def get_serializer_class(self):
        """
        Decide serializer based on action
        """
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return UserProfileSerializer
        return UserSerializer
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer