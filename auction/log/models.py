from django.db import models
from offer import Offer
from user import User

class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()
    end_point = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField() 
    