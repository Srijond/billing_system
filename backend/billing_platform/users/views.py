from django.shortcuts import render
from rest_framework.decorators import action
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from packages.models import SubscriptionPackage
from subscriptions.models import UserSubscription
from invoices.models import Invoice, InvoiceItem
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

    @transaction.atomic
    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def onboard(self, request):
        """
        Onboard a new user with subscription packages
        """
        # Validate user data
        user_serializer = UserSerializer(data=request.data)
        if not user_serializer.is_valid():
            return Response(
                user_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get and validate packages
        package_ids = request.data.get('package_ids', [])
        if not package_ids:
            return Response(
                {'package_ids': 'At least one package must be assigned'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        packages = SubscriptionPackage.objects.filter(
            id__in=package_ids,
            is_active=True
        )
        
        if not packages.exists():
            return Response(
                {'package_ids': 'No valid active packages found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if packages.count() != len(package_ids):
            return Response(
                {'package_ids': 'Some packages are invalid or inactive'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user
        user = user_serializer.save(onboarded_by=request.user)
        
        # Assign packages
        for package in packages:
            UserSubscription.objects.create(
                user=user,
                package=package,
                assigned_by=request.user
            )
        
        # Generate invoice
        invoice = Invoice.objects.create(
            user=user,
            generated_by=request.user,
            total_amount=0
        )
        
        total = 0
        for package in packages:
            InvoiceItem.objects.create(
                invoice=invoice,
                package=package,
                package_name=package.name,
                package_type=package.type,
                price=package.price
            )
            total += package.price
        
        invoice.total_amount = total
        invoice.save()
        
        return Response({
            'user': UserDetailSerializer(user).data,
            'invoice': {
                'id': invoice.id,
                'invoice_number': invoice.invoice_number,
                'total_amount': str(invoice.total_amount)
            }
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer