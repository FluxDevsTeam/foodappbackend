from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register(r'profiles', views.ProfileViewSet, basename='profile')
router.register(r'vendors', views.VendorViewSet, basename='vendor')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'carts', views.CartViewSet, basename='cart')
router.register(r'wishlists', views.WishlistViewSet, basename='wishlist')
router.register(r'rider-earnings', views.RiderEarningsViewSet, basename='rider-earnings')
router.register(r'orders', views.OrderViewSet, basename='order')  # Added OrderViewSet
router.register(r'riders', views.RiderViewSet, basename='rider')

# Nested routers for products
products_router = routers.NestedSimpleRouter(router, r'products', lookup='product')
products_router.register(r'comments', views.ProductCommentViewSet, basename='product-comments')
products_router.register(r'food-ratings', views.ProductFoodRatingViewSet, basename='product-food-ratings')

# Nested routers for orders
orders_router = routers.NestedSimpleRouter(router, r'orders', lookup='order')
orders_router.register(r'items', views.OrderItemViewSet, basename='order-items')

# Nested routers for riders
riders_router = routers.NestedSimpleRouter(router, r'riders', lookup='rider')
riders_router.register(r'delivery-ratings', views.RiderDeliveryRatingViewSet, basename='rider-delivery-ratings')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(orders_router.urls)),
    path('', include(riders_router.urls)),
]