from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'address', 'is_admin', 'is_active',
            'date_joined', 'onboarded_by', 'password'
        ]
        read_only_fields = ['id', 'date_joined', 'onboarded_by']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    onboarded_by_email = serializers.EmailField(
        source='onboarded_by.email',
        read_only=True
    )
    # subscription_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'address', 'is_admin', 'is_active',
            'date_joined', 'onboarded_by', 'onboarded_by_email',
            
        ]
        read_only_fields = ['id', 'date_joined', 'onboarded_by']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    # def get_subscription_count(self, obj):
    #     pass

class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'address', 'is_admin', 'date_joined'
        ]
        read_only_fields = [
            'id', 'email', 'is_admin', 'date_joined'
        ]
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    

