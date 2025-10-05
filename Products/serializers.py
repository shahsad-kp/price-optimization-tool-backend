from collections import OrderedDict
from datetime import date

from rest_framework.fields import IntegerField, DecimalField
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer, Serializer

from Products.models import Products, ProductSales
from Products.utils import generate_demand_forecast, calculate_optimal_price


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

    def update(self, instance: Products, validated_data: OrderedDict) -> Products:
        instance: Products = super().update(instance, validated_data)
        today = date.today()
        ProductSales.objects.update_or_create(
            product=instance,
            date=today,
            defaults={
                'units_sold': instance.units_sold,
                'selling_price': instance.selling_price,
            }
        )
        return instance

    def create(self, validated_data: OrderedDict) -> Products:
        instance = super().create(validated_data)
        ProductSales.objects.create(
            product=instance,
            units_sold=instance.units_sold,
            selling_price=instance.selling_price,
        )
        return instance

    def to_representation(self, instance: Products) -> OrderedDict:
        data = super().to_representation(instance)
        request: Request = self.context.get('request')
        with_demand_forecast = request.query_params.get('with_demand_forecast', 'false')
        if with_demand_forecast.lower() in ('true', '1', 'yes'):
            number_of_days = request.query_params.get('demand_forecast_interval', '30')
            if number_of_days.isdigit():
                number_of_days = int(number_of_days)
            else:
                number_of_days = 30
            data['demand_forecast'] = generate_demand_forecast(instance, number_of_days)
        if self.context.get('add-complete-sales', False):
            data['complete_sales'] = ProductSalesSerializer(instance.sales.all(), many=True).data
        return data


class ProductSalesSerializer(ModelSerializer):
    class Meta:
        model = ProductSales
        fields = [
            'product_id',
            'date',
            'units_sold',
            'selling_price',
        ]


class PriceOptimizationSerializer(Serializer):
    id = IntegerField()
    current_price = DecimalField(max_digits=10, decimal_places=2, write_only=True)
    total_forecasted_demand: int = IntegerField(write_only=True)
    cost_price = DecimalField(max_digits=10, decimal_places=2, write_only=True)
    optimal_price = DecimalField(max_digits=10, decimal_places=2, read_only=True)
    max_profit = DecimalField(max_digits=10, decimal_places=2, read_only=True)

    def create(self, validated_data: OrderedDict):
        is_list = isinstance(validated_data, list)
        if not is_list:
            validated_data = [validated_data]
        results = []
        for item in validated_data:
            result = calculate_optimal_price(
                current_price=float(item['current_price']),
                total_forecasted_demand=item['total_forecasted_demand'],
                cost_price=float(item['cost_price']),
            )
            data = {
                'id': item['id'],
                'optimal_price': result['optimal_price'],
                'max_profit': result['max_profit'],
            }
            results.append(data)
        return results if is_list else results[0]
