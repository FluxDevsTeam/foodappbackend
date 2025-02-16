from django.db import models
from django.conf import settings
from orders.models import Order


class RiderEarnings(models.Model):
    rider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='earnings')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount_earned = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Earnings for {self.rider.username}'


class DeliveryRating(models.Model):
    rider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='delivery_ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_delivery_ratings')
    rating = models.PositiveIntegerField(default=1)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'DeliveryRating by {self.user.username} for {self.rider.username}'
