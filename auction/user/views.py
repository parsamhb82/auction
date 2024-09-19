from django.shortcuts import render
from .models import *
from .serilizers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class Login(TokenObtainPairView):
    pass

class RefreshToken(TokenRefreshView):
    pass
class ProviderRegisterView(CreateAPIView):

    serializer_class = RegisterSerializer
    queryset = Provider.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        Provider.objects.create(user=serializer.instance)

class CustomerRegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = Customer.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        Customer.objects.create(user=serializer.instance)

        

