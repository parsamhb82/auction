from django.utils import timezone
from django.http import JsonResponse
from log.models import Log
from django.views import View

class LogView(View):
    def get(self, request, *args, **kwargs):
        ip_address = request.META.get('REMOTE_ADDR', None)
        if request.user.is_authenticated:
            Log.objects.create(
                user=request.user,
                time=timezone.now(),
                end_point=request.path,
                ip_address=ip_address
            )
        logs = Log.objects.all().values('user__username', 'time', 'end_point', 'ip_address')
        log_list = list(logs)
        return JsonResponse(log_list, safe=False)