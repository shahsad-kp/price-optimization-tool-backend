from datetime import date

from django.core.validators import MaxValueValidator
from django.db.models import Model, AutoField, CharField, DecimalField, IntegerField, PositiveIntegerField, ForeignKey, \
    CASCADE, DateField


class Products(Model):
    product_id = AutoField(primary_key=True)
    name = CharField(max_length=100)
    description = CharField(max_length=500)
    cost_price = DecimalField(decimal_places=2, max_digits=10)
    selling_price = DecimalField(decimal_places=2, max_digits=10)
    category = CharField(max_length=100)
    stock_available = IntegerField(default=0)
    units_sold = IntegerField(default=0)
    customer_rating = PositiveIntegerField(
        default=0,
        validators=[
            MaxValueValidator(5)
        ]
    )
    demand_forecast = PositiveIntegerField()
    optimized_price = DecimalField(decimal_places=2, max_digits=10, null=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Products'
        verbose_name_plural = 'Products'
        ordering = ('name',)


class ProductSales(Model):
    sales_id = AutoField(primary_key=True)
    product = ForeignKey(
        'Products',
        on_delete=CASCADE,
        related_name='sales'
    )
    date = DateField(default=date.today)
    units_sold = PositiveIntegerField(default=0)
    selling_price = DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        db_table = 'product_sales'
        verbose_name = 'Product Sale'
        verbose_name_plural = 'Product Sales'
        ordering = ('date',)
        unique_together = ('product', 'date')
