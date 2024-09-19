from django.urls import path
from .views import Login, RefreshToken, ProviderRegisterView, CustomerRegisterView

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('refresh/', RefreshToken.as_view(), name='refresh'),
    path('provider/register/', ProviderRegisterView.as_view(), name='provider-register'),
    path('customer/register/', CustomerRegisterView.as_view(), name='customer-register'),

]