from django.conf import settings
from django.utils.safestring import mark_safe

LOGOUT_TIMEOUT_SCRIPT_PATTERN = """
<script>
    window.onload = function () {
        try{
            if(autoLogoutTime != 'undefined' && autoLogoutTime != null && !Number.isNaN(autoLogoutTime))
                countdownSeconds = autoLogoutTime;
            updateCountdown();
        }catch(error){
                console.error('An error occurred:', error.message);
        }
    };
    document.addEventListener('click', resetCountdown);
</script>
"""


def _trim(s: str) -> str:
    return ''.join([line.strip() for line in s.split('\n')])


def auto_logout_client(request):
    if request.user.is_anonymous:
        return {}

    options = getattr(settings, 'AUTO_LOGOUT')
    if not options:
        return {}

    ctx = {}

    if options.get('REDIRECT_TO_LOGIN_IMMEDIATELY'):
        ctx['redirect_to_login_immediately'] = mark_safe(_trim(LOGOUT_TIMEOUT_SCRIPT_PATTERN))

    return ctx
