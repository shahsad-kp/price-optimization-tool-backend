from django.db.models import Q
from django_filters import FilterSet, CharFilter, OrderingFilter

from Products.models import Products


class ProductFilterSet(FilterSet):
    search = CharFilter(method='filter_search')
    ordering = OrderingFilter(
        fields=(
            ('selling_price', 'selling_price'),
            ('customer_rating', 'customer_rating'),
            ('name', 'name'),
        ),
    )

    class Meta:
        model = Products
        fields = [
            'category',
            'customer_rating',
            'selling_price'
        ]

    @staticmethod
    def filter_search(queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))
