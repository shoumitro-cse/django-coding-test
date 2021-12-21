import django_filters
from product.models import Product


class ProductFilter(django_filters.FilterSet):
    created = django_filters.CharFilter(method='created_filter')
    variant_title = django_filters.CharFilter(method='variant_title_filter')
    price_from = django_filters.CharFilter(method='price_from_filter')
    price_to = django_filters.CharFilter(method='price_to_filter')

    def variant_title_filter(self, queryset, name, value):
        return queryset.filter(product_variants__variant_title__icontains=value).distinct()

    def price_from_filter(self, queryset, name, value):
        return queryset.filter(product_variant_prices__price__gt=value).distinct()

    def price_to_filter(self, queryset, name, value):
        return queryset.filter(product_variant_prices__price__lt=value).distinct()

    def created_filter(self, queryset, name, value):
        return queryset.filter(created__gt=value).distinct()

    class Meta:
        model = Product
        fields = ['title', "created"]

