from django.utils import timezone
from log.models import Log

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated: 
            ip_address = request.META.get('REMOTE_ADDR', None)
            end_point = request.path
            Log.objects.create(
                user=request.user,
                time=timezone.now(),
                end_point=end_point,
                ip_address=ip_address
            )
        return response
