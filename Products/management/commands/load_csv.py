import csv

from django.core.management import BaseCommand

from Products.models import Products


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('product data.csv', mode='r', newline='') as file:
            csv_dict_reader = csv.DictReader(file)
            data_as_dict = []
            for row in csv_dict_reader:
                row.pop('product_id')
                data_as_dict.append(row)

            Products.objects.bulk_create([
                Products(**row)
                for row in data_as_dict
            ])

