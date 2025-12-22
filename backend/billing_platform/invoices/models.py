from django.db import models
from django.core.validators import MinValueValidator
from users.models import User
from packages.models import SubscriptionPackage

class Invoice(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='invoices'
    )
    invoice_number = models.CharField(max_length=50, unique=True, db_index=True)
    total_amount = models.DecimalField(
        max_digits=30,
        decimal_places=6,
        validators=[MinValueValidator(0)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='generated_invoices'
    )
    
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.user.email}"
    
    def calculate_total(self):
        """Calculate total from invoice items"""
        return sum(item.price for item in self.items.all())
    
    def save(self, *args, **kwargs):
        # Generate invoice number if not set
        if not self.invoice_number:
            from django.utils import timezone
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.invoice_number = f"INV-{timestamp}-{self.user.id}"
        super().save(*args, **kwargs)

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items'
    )
    package = models.ForeignKey(
        SubscriptionPackage,
        on_delete=models.PROTECT,
        related_name='invoice_items'
    )
    package_name = models.CharField(max_length=100)
    package_type = models.CharField(max_length=20)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.package_name}"
    
    def save(self, *args, **kwargs):
        # Store package details for immutability
        if not self.package_name:
            self.package_name = self.package.name
        if not self.package_type:
            self.package_type = self.package.type
        if not self.price:
            self.price = self.package.price
        super().save(*args, **kwargs)