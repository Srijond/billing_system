from django.shortcuts import render
from users.models import User
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import SubscriptionPackage
from .serializers import (
    SubscriptionPackageSerializer,
    SubscriptionPackageListSerializer
)
from users.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated

class SubscriptionPackageViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPackage.objects.select_related('created_by').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['type', 'name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SubscriptionPackageListSerializer
        return SubscriptionPackageSerializer
    
    
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        # self.request.user
        
        # Regular users can only see active packages
        if not (user.is_admin or user.is_superuser):
            queryset = queryset.filter(is_active=True)
        
        return queryset
    
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)
    