from .models import UserSubscription
from packages.serializers import SubscriptionPackageListSerializer
from rest_framework import serializers


class UserSubscriptionSerializer(serializers.ModelSerializer):
    package_details = SubscriptionPackageListSerializer(
        source='package',
        read_only=True
    )
    user_email = serializers.EmailField(source='user.email', read_only=True)
    assigned_by_email = serializers.EmailField(
        source='assigned_by.email',
        read_only=True
    )
    
    class Meta:
        model = UserSubscription
        fields = [
            'id', 'user', 'user_email', 'package', 'package_details',
            'assigned_by', 'assigned_by_email', 'assigned_at','notes'
        ]
        read_only_fields = ['id', 'assigned_by', 'assigned_at']
    
    def validate(self, data):
        # Check if package is active
        package = data.get('package')
        if package and not package.is_active:
            raise serializers.ValidationError({
                'package': 'Cannot assign inactive package'
            })
        
        # Check for duplicate subscription
        user = data.get('user')
        if user and package:
            exists = UserSubscription.objects.filter(
                user=user,
                package=package,
            ).exists()
            if exists:
                raise serializers.ValidationError({
                    'package': 'User already has this package assigned'
                })
        
        return data

class UserSubscriptionListSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(source='package.name', read_only=True)
    package_type = serializers.CharField(
        source='package.get_type_display',
        read_only=True
    )
    package_price = serializers.DecimalField(
        source='package.price',
        max_digits=30,
        decimal_places=6,
        read_only=True
    )
    
    class Meta:
        model = UserSubscription
        fields = [
            'id', 'package', 'package_name', 'package_type',
            'package_price', 'assigned_at'
        ]