from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView,DestroyAPIView
from .models import *
from .serilizers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import datetime
from django.utils.timezone import now

class CreateAuction(CreateAPIView):
    serializer_class = AuctionCreatSerializer
    queryset = Auction.objects.all()

    def post(self, request, *args, **kwargs):
        user = request.user
        provider = user.provider
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(provider=provider)

class CreateProduct(CreateAPIView):
    serializer_class = ProductCreatSerilizer
    queryset = Product.objects.all()

    def post(self, request, *args, **kwargs):
        user = request.user
        provider = user.provider
        auction = Auction.objects.get(id=request.data['auction'])
        if auction.provider != provider:
            return Response({'message': 'you are not the provider of this auction'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(auction=auction)
class CreateOffer(CreateAPIView):
    serializer_class = OfferCreatSerilizer
    queryset = Offer.objects.all()

    def post(self, request, *args, **kwargs):
        customer = self.request.customer
        time = now()
        product = Product.objects.get(id=request.data['product'])
        if product.end_time < time:
            return Response({'message': 'the auction is over'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        given_price = serializer.validated_data['price']
        if given_price < product.start_price:
            return Response({'message': 'the price is lower than the start price'}, status=status.HTTP_400_BAD_REQUEST)
        if given_price < product.current_price:
            return Response({'message': 'the price is lower than the current price'}, status=status.HTTP_400_BAD_REQUEST)
        if product.current_price != 0 and given_price > product.current_price:
            product.current_price = given_price
            product.save()
            serializer.save(customer=customer, product=product)
        if product.current_price == 0 and given_price >= product.start_price:
            product.current_price = given_price
            product.end_time += datetime.timedelta(minutes=10)
            product.save()
            serializer.save(customer=customer, product=product)

class AuctionDestroyView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try:
            # Get the auction instance
            auction = Auction.objects.get(pk=pk)
        except Auction.DoesNotExist:
            return Response({"error": "Auction not found."}, status=status.HTTP_404_NOT_FOUND)

        # Use the serializer to handle deletion logic
        serializer = AuctionDeleteSerializer()
        serializer.delete(auction)

        return Response({"message": "Auction and related products (if no offers) deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class FinishedProductsView(ListAPIView):
    serializer_class = ProductCreatSerilizer
    queryset = Product.objects.all()

    def get_queryset(self):
        return Product.objects.filter(end_time__lt=now())
    
class UnfinishedProductsView(ListAPIView):
    serializer_class = ProductCreatSerilizer
    queryset = Product.objects.all()

    def get_queryset(self):
        return Product.objects.filter(end_time__gte=now())
    




        




