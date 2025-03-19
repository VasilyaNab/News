from django.utils import timezone
import pytz
from django.utils.deprecation import MiddlewareMixin

class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'django_timezone' not in request.session:
            request.session['django_timezone'] = 'UTC'
        tz = request.session.get('django_timezone', 'UTC')
        timezone.activate(pytz.timezone(tz))
        current_time = timezone.now().astimezone(pytz.timezone(tz))
        request.current_time = current_time
        if 6 <= current_time.hour < 18:
            request.theme = 'light'
        else:
            request.theme = 'dark'
        request.session['theme'] = request.theme

    def process_template_response(self, request, response):
        if hasattr(response, 'context_data'):
            response.context_data['current_time'] = getattr(request, 'current_time', None)
        return response