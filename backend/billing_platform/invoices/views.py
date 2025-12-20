from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Invoice
from .serializers import InvoiceSerializer, InvoiceListSerializer
from users.permissions import IsOwnerOrAdmin

class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only viewset for invoices
    Invoices are immutable after creation
    """
    queryset = Invoice.objects.select_related(
        'user', 'generated_by'
    ).prefetch_related('items__package').all()
    permission_classes = [IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['user']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return InvoiceListSerializer
        return InvoiceSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        
        # Regular users see only their invoices
        if not (user.is_admin or user.is_superuser):
            queryset = queryset.filter(user=user)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        user = request.user        
        response = super().list(request, *args, **kwargs)
        
       
        
        return response