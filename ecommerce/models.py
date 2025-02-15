from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# User Profile (For additional fields)
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
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor')
    address = models.TextField()
    phone = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Product Model
class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Cart Model
class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart of {self.customer.username}'


# Cart Item Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in cart'


# Wishlist Model
class Wishlist(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer.username} - {self.product.name}'


# Discount Model
class Discount(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='discounts')
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.PositiveIntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.code


# Promotion Model
class Promotion(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='promotions')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_percent = models.PositiveIntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return f'Promotion on {self.product.name}'


# Notification Model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user.username}'


# Rider Earnings Model
class RiderEarnings(models.Model):
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='earnings')
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    amount_earned = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Earnings for {self.rider.username}'


# Referral Model
class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referred_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referred_by')
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.referrer.username} referred {self.referred_user.username}'
