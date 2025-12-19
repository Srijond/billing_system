from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import SubscriptionPackage

class SubscriptionPackageSerializer(serializers.ModelSerializer):
    created_by_email = serializers.EmailField(
        source='created_by.email',
        read_only=True
    )
    type_display = serializers.CharField(
        source='get_type_display',
        read_only=True
    )
    
    class Meta:
        model = SubscriptionPackage
        fields = [
            'id', 'name', 'type', 'type_display', 'description',
            'price', 'is_active', 'created_at', 'updated_at',
            'created_by', 'created_by_email'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value

class SubscriptionPackageListSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(
        source='get_type_display',
        read_only=True
    )
    
    class Meta:
        model = SubscriptionPackage
        fields = [
            'id', 'name', 'type', 'type_display',
            'price', 'is_active'
        ]