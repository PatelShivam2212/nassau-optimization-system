import pandas as pd
from datetime import datetime
from django.core.management.base import BaseCommand
from optimization.models import Factory, Product, Order


class Command(BaseCommand):
    help = 'Imports Nassau Candy Order data from CSV'

    def handle(self, *args, **kwargs):
        df = pd.read_csv('Nassau Candy Distributor.csv')

        # Convert dates
        df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
        df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)

        self.stdout.write("Importing Orders...")

        for _, row in df.iterrows():
            # Find the product (assuming you seeded products first)
            try:
                product = Product.objects.get(name=row['Product Name'])

                Order.objects.create(
                    order_id=row['Order ID'],
                    order_date=row['Order Date'].date(),
                    ship_date=row['Ship Date'].date(),
                    ship_mode=row['Ship Mode'],
                    city=row['City'],
                    region=row['Region'],
                    product=product,
                    sales=row['Sales'],
                    gross_profit=row['Gross Profit']
                )
            except Product.DoesNotExist:
                continue

        self.stdout.write(self.style.SUCCESS(f"Successfully imported {len(df)} orders!"))