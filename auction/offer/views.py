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
from .permissions import IsProvider, IsCustomer
import requests
from datetime import date
import json

class CreateAuction(CreateAPIView):
    permission_classes = [IsAuthenticated, IsProvider]
    serializer_class = AuctionCreatSerializer
    queryset = Auction.objects.all()

    def post(self, request, *args, **kwargs):
        user = request.user
        provider = user.provider
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(provider=provider)

class CreateProduct(CreateAPIView):
    permission_classes = [IsAuthenticated, IsProvider]
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
    permission_classes = [IsAuthenticated, IsCustomer]
    serializer_class = OfferCreatSerilizer
    queryset = Offer.objects.all()

    def post(self, request, *args, **kwargs):

        today = date.today()
        today_list = today.split('-')
        url = f"https://holidayapi.ir/gregorian/{today_list[0]}/{today_list[1]}/{today_list[2]}"
        response = requests.get(url)
        json_file = json.loads(response.content)
        is_holiday = json_file['is_holiday']
        if is_holiday:
            return Response({'message': 'today is a holiday'}, status=status.HTTP_400_BAD_REQUEST)
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
    permission_classes = [IsAuthenticated, IsProvider]
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
    permission_classes = [IsAuthenticated]
    serializer_class = ProductCreatSerilizer
    queryset = Product.objects.all()

    def get_queryset(self):
        return Product.objects.filter(end_time__lt=now())
    
class UnfinishedProductsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductCreatSerilizer
    queryset = Product.objects.all()

    def get_queryset(self):
        return Product.objects.filter(end_time__gte=now())
    




        




