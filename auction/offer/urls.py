from django.urls import path

from .views import CreateAuction, CreateProduct, CreateOffer, AuctionDestroyView, FinishedProductsView, UnfinishedProductsView

urlpatterns = [
    path('create-auction/', CreateAuction.as_view(), name='create-auction'),
    path('create-product/', CreateProduct.as_view(), name='create-product'),
    path('create-offer/', CreateOffer.as_view(), name='create-offer'),
    path('auction/<int:pk>/destroy/', AuctionDestroyView.as_view(), name='auction-destroy'),
    path('finished-products/', FinishedProductsView.as_view(), name='finished-products'),
    path('unfinished-products/', UnfinishedProductsView.as_view(), name='unfinished-products'),
]