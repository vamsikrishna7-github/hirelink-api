# subscriptions/models.py
from django.db import models
from django.conf import settings
from django.db.models import Q

CURRENCY_CHOICES = [
    ('INR', 'Indian Rupee'),
    ('USD', 'US Dollar'),
    ('EUR', 'Euro'),
]

USER_TYPE_CHOICES = [
    ('employer', 'Employer'),
    ('consultancy', 'Consultancy'),
]

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.JSONField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.name} ({self.currency} {self.price})"

class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], condition=Q(active=True), name='unique_active_subscription_per_user')
        ]

    def __str__(self):
        return f"{self.user} - {self.plan} - {'Active' if self.active else 'Inactive'}"

