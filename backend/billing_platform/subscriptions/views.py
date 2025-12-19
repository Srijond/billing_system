from django.shortcuts import render
from users.models import User
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import UserSubscription
from .serializers import (
    UserSubscriptionSerializer,
    UserSubscriptionListSerializer
)
# from apps.users.permissions import IsAdminUser, IsOwnerOrAdmin

# Create your views here.
class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.select_related(
        'user', 'package', 'assigned_by'
    ).all()
    # permission_classes = [IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'package']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UserSubscriptionListSerializer
        return UserSubscriptionSerializer
    
    # def get_permissions(self):
    #     if self.action in ['create', 'update', 'partial_update', 'destroy']:
    #         return [IsAdminUser()]
    #     return [IsOwnerOrAdmin()]
    
    def get_queryset(self):
        user = User.objects.get(id=1) 
        # self.request.user
        queryset = self.queryset
        
        # Regular users see only their subscriptions
        if not (user.is_admin or user.is_superuser):
            queryset = queryset.filter(user=user)
        
        return queryset
    
    def perform_create(self, serializer):
        user = User.objects.get(id=1) 
        # self.request.user
        subscription = serializer.save(assigned_by=user)
    