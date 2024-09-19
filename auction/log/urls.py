from django.urls import path
from log.views import LogCreate, LogView  

urlpatterns = [
    path('logs/create/', LogCreate.as_view(), name='log-create'),
    path('logs/', LogView.as_view(), name='log-list'),
]
