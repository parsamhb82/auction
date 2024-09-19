from rest_framework import serializers
from .models import *

class AuctionCreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ['name']

class ProductCreatSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'picture', 'auction', 'start_time', 'end_time', 'start_price']

class OfferCreatSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['product', 'price']

class AuctionDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ['id', 'provider', 'name']

    def delete(self, instance):
        products = Product.objects.filter(auction=instance)

        # Check if products have offers
        for product in products:
            if not Offer.objects.filter(product=product).exists():
                product.delete()

        # Now delete the auction
        instance.delete()
        return instance


