from django.db import models

# Create your models here.
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class SubscriptionPackage(models.Model):
    PACKAGE_TYPES = [
        ('isp', 'ISP'),
        ('realip', 'Real IP'),
        ('tv', 'TV'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=PACKAGE_TYPES)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=30,
        decimal_places=6,
        validators=[MinValueValidator(0)]
    )
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_packages'
    )
    
    class Meta:
        ordering = ['type', 'name']
        
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
    