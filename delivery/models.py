from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    USER_TYPES = [
        ('customer', 'Customer'),
        ('rider', 'Rider'),
        ('vendor', 'Vendor'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='customer')

    def __str__(self):
        return self.user.username


# Vendor Model
class RiderEarnings(models.Model):
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='earnings')
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    amount_earned = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Earnings for {self.rider.username}'


