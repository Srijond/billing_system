from .models import Invoice, InvoiceItem
from rest_framework import serializers

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = [
            'id', 'package', 'package_name', 'package_type', 'price'
        ]
        read_only_fields = [
            'id', 'package_name', 'package_type', 'price'
        ]

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(
        source='user.get_full_name',
        read_only=True
    )
    generated_by_email = serializers.EmailField(
        source='generated_by.email',
        read_only=True
    )
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'user', 'user_email', 'user_name',
            'total_amount', 'created_at', 'generated_by',
            'generated_by_email', 'notes', 'items'
        ]
        read_only_fields = [
            'id', 'invoice_number', 'created_at',
            'generated_by', 'total_amount'
        ]

class InvoiceListSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    item_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'user_email',
            'total_amount', 'created_at', 'item_count'
        ]
    
    def get_item_count(self, obj):
        return obj.items.count()