from django.utils import timezone
from log.models import Log
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import LogSerializer  


class LogCreate(CreateAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        ip_address = self.request.META.get('REMOTE_ADDR', None)
        serializer.save(
            user=self.request.user,
            time=timezone.now(),
            end_point=self.request.path,
            ip_address=ip_address
        )
        def post(self, request, *args, **kwargs):
            response = super().post(request, *args, **kwargs)
            response.data = {
                'message': 'Log created successfully.',
                'log': response.data
        }
        return Response


class LogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logs = Log.objects.all().values('user__username', 'time', 'end_point', 'ip_address')
        log_list = list(logs)
        return Response(log_list)
