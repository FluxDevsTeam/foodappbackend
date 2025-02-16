from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.conf import settings

from delivery.models import RiderEarnings, DeliveryRating
from ecommerce.models import Product, Cart, Profile, CartItem, Wishlist, Comment, FoodRating
from orders.models import Order, OrderItem
from vendor.models import Vendor
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user']


class VendorSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Vendor
        fields = '__all__'
        read_only_fields = ['owner', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['vendor', 'created_at']


class CartSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'created_at']
        read_only_fields = ['customer', 'created_at']


class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ['cart', 'added_at']


class WishlistSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = '__all__'
        read_only_fields = ['customer', 'added_at']


class RiderEarningsSerializer(serializers.ModelSerializer):
    rider = UserSerializer(read_only=True)

    class Meta:
        model = RiderEarnings
        fields = '__all__'
        read_only_fields = ['rider', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'rating', 'created_at']
        read_only_fields = ['user', 'created_at']


class FoodRatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = FoodRating
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']


class DeliveryRatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DeliveryRating
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = [
            'user', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']
        read_only_fields = ['order', 'price']


class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    vendor = VendorSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'vendor', 'status', 'total_price',
            'created_at', 'updated_at', 'items'
        ]
        read_only_fields = ['customer', 'vendor', 'total_price', 'created_at', 'updated_at']