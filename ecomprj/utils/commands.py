from django.http import HttpRequest
from django_auto_logout.utils import now


def reset_session_timeout(*params):
    if len(params) >= 2:
        request = params[0]
        request_str = params[1]
        executable = False
        if isinstance(request, HttpRequest):
            print("The object is an instance of HttpRequest")
            executable = True
        elif isinstance(request_str,str) and request_str.lower() == 'request':
            print("The object is an instance of HttpRequest")
            executable = True
        else:
            print("The object is not an instance of HttpRequest")

        if executable:
            current_time = now()
            request.session['django_auto_logout_last_request'] = current_time.isoformat()
