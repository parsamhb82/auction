from django.db import models
from user.models import Provider,  Customer

class Auction(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

class Product(models.Model):
    name = models.CharField(max_length=255)
    picture = models.ImageField()
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    start_price = models.FloatField()
    current_price = models.FloatField(blank=True, null=True)

class Offer(models.Mode):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()