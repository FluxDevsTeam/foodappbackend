import django_filters
from ecommerce.models import Product
from orders.models import Order
from vendor.models import Vendor
from django.conf import settings


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    vendor = django_filters.ModelChoiceFilter(queryset=Vendor.objects.all())

    class Meta:
        model = Product
        fields = ['name', 'vendor', 'is_available']


class OrderFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='iexact')
    min_total_price = django_filters.NumberFilter(field_name='total_price', lookup_expr='gte')
    max_total_price = django_filters.NumberFilter(field_name='total_price', lookup_expr='lte')
    customer = django_filters.ModelChoiceFilter(queryset=settings.AUTH_USER_MODEL.objects.filter(profile__user_type='customer'))
    vendor = django_filters.ModelChoiceFilter(queryset=Vendor.objects.all())

    class Meta:
        model = Order
        fields = ['status', 'customer', 'vendor']