from django.urls import path
from . import views 

urlpatterns = [
    path('logs/', views.my_view, name='log_list'),
]
