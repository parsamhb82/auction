from rest_framework import serializers
from log.models import Log

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['user', 'time', 'end_point', 'ip_address']
