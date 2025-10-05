from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from Products.filters import ProductFilterSet
from Products.models import Products
from Products.serializers import ProductSerializer, ProductSalesSerializer, PriceOptimizationSerializer


class ProductViewSet(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilterSet
    permission_classes = (AllowAny,)

    @action(
        detail=False,
        methods=['get'],
        url_path='sales',
        permission_classes=(AllowAny,)
    )
    def with_complete_sales(self, request: Request, *args, **kwargs):
        queryset = self.get_queryset()
        product_ids = request.query_params.getlist('product_ids', [])
        if not isinstance(product_ids, list):
            product_ids = [str(product_ids)]
        queryset = queryset.filter(product_id__in=product_ids)
        serializer = ProductSerializer(queryset, many=True, context={'add-complete-sales': True, 'request': request})
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['post'],
        url_path='price-optimize',
        permission_classes=(AllowAny,)
    )
    def optimize(self, request: Request):
        data = request.data
        ser = PriceOptimizationSerializer(data=data, many=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @action(
        detail=True,
        methods=['get'],
        url_path='sales',
        permission_classes=(AllowAny,)
    )
    def sales(self, *args, **kwargs):
        products: Products = self.get_object()
        ser = ProductSalesSerializer(products.sales.all(), many=True)
        return Response(ser.data)
