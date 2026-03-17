from django.db import models


class Factory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    division = models.CharField(max_length=100)
    # This links the product to its current "Legacy" factory
    current_factory = models.ForeignKey(Factory, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f"{self.name} ({self.division})"


class Order(models.Model):
    order_id = models.CharField(max_length=100)
    order_date = models.DateField()
    ship_date = models.DateField()
    ship_mode = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sales = models.FloatField()
    gross_profit = models.FloatField()

    def __str__(self):
        return self.order_id


from django.db import models

# Create your models here.
