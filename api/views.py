from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from orders.models import OrderItem, Order
from .serializers import (
    ProfileSerializer, VendorSerializer, ProductSerializer,
    CartSerializer, CartItemSerializer, WishlistSerializer,
    RiderEarningsSerializer, CommentSerializer,
    FoodRatingSerializer, DeliveryRatingSerializer, UserSerializer, OrderItemSerializer, OrderSerializer
)
from django.contrib.auth import get_user_model
from delivery.models import RiderEarnings, DeliveryRating
from ecommerce.models import Product, Cart, Profile, CartItem, Wishlist, Comment, FoodRating
from vendor.models import Vendor

User = get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        vendor = get_object_or_404(Vendor, owner=self.request.user)
        serializer.save(vendor=vendor)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__customer=self.request.user)

    def perform_create(self, serializer):
        cart = get_object_or_404(Cart, customer=self.request.user)
        serializer.save(cart=cart)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Customers can view their own orders
        if self.request.user.profile.user_type == 'customer':
            return Order.objects.filter(customer=self.request.user)
        # Vendors can view orders assigned to them
        elif self.request.user.profile.user_type == 'vendor':
            return Order.objects.filter(vendor__owner=self.request.user)
        # Admins can view all orders
        return Order.objects.all()

    def perform_create(self, serializer):
        # Automatically set the customer to the logged-in user
        serializer.save(customer=self.request.user)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order_id=self.kwargs['order_pk'])

    def perform_create(self, serializer):
        order = get_object_or_404(Order, pk=self.kwargs['order_pk'])
        product = get_object_or_404(Product, pk=serializer.validated_data['product'].id)
        # Calculate the price based on the product's current price
        serializer.save(order=order, price=product.price * serializer.validated_data['quantity'])


class ProductCommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(product_id=self.kwargs['product_pk'])

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs['product_pk'])
        serializer.save(user=self.request.user, product=product)


class ProductFoodRatingViewSet(viewsets.ModelViewSet):
    serializer_class = FoodRatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FoodRating.objects.filter(product_id=self.kwargs['product_pk'])

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs['product_pk'])
        serializer.save(user=self.request.user, product=product)


class RiderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter(profile__user_type='rider')


class RiderDeliveryRatingViewSet(viewsets.ModelViewSet):
    serializer_class = DeliveryRatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DeliveryRating.objects.filter(rider_id=self.kwargs['rider_pk'])

    def perform_create(self, serializer):
        rider = get_object_or_404(User, pk=self.kwargs['rider_pk'])
        serializer.save(user=self.request.user, rider=rider)


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class RiderEarningsViewSet(viewsets.ModelViewSet):
    serializer_class = RiderEarningsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RiderEarnings.objects.filter(rider=self.request.user)

    def perform_create(self, serializer):
        serializer.save(rider=self.request.user)
