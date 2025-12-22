from django.db import models
from django.core.exceptions import ValidationError
from users.models import User
from packages.models import SubscriptionPackage

class UserSubscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    package = models.ForeignKey(
        SubscriptionPackage,
        on_delete=models.PROTECT,
        related_name='user_subscriptions'
    )
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_subscriptions'
    )
    
    assigned_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-assigned_at']
        unique_together = [['user', 'package']]
    
    def __str__(self):
        return f"{self.user.email} - {self.package.name}"
    
    def clean(self):
        # Validate package is active
        if self.package and not self.package.is_active:
            raise ValidationError({
                'package': 'Cannot assign inactive package to user'
            })
        
        # Check for duplicate active subscription
        if  self.pk is None:
            exists = UserSubscription.objects.filter(
                user=self.user,
                package=self.package
            ).exists()
            if exists:
                raise ValidationError({
                    'package': 'User already has this package assigned'
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)