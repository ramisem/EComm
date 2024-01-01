from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect
import utils


def check_session_timeout(request):
    auto_logout_message = None
    if hasattr(settings, 'AUTO_LOGOUT'):
        auto_logout_prop = settings.AUTO_LOGOUT
    else:
        raise utils.product_exception.ProductException(request=request,
                                                       message=f'Auto Logout property has not been configured in settings.py\n '
                                                               f'Please check log for more details.',
                                                       custom_message=f'Auto Logout property has not been configured in settings.py.\n'
                                                                      f'Please check log for more details.',
                                                       mode='redirect', page='userauths:sign-in',
                                                       logoff=True)
    if auto_logout_prop is not None:
        auto_logout_message = auto_logout_prop['MESSAGE']
    if auto_logout_message is not None:
        auto_logged_out = any(auto_logout_message in message.message for message in messages.get_messages(request))
    else:
        raise utils.product_exception.ProductException(request=request,
                                                       message=f'Auto Logout property has not been configured in settings.py.\n '
                                                               f'Please provide the Message in the Auto-Logout property.',
                                                       custom_message=f'Auto Logout property has not been configured in settings.py\n'
                                                                      f'Please provide the Message in the Auto-Logout property',
                                                       mode='redirect', page='userauths:sign-in',
                                                       logoff=True)
    return auto_logged_out


def set_next_url(request):
    preserved_url = request.build_absolute_uri()
    if preserved_url is not None:
        request.session['preserved_url'] = preserved_url
        request.session.set_expiry(int(getattr(settings, 'SESSION_CUSTOM_COOKIE_AGE', '300')))
    return


def get_next_url(request):
    return request.session.get('preserved_url', None)


def redirect_to_next_url(request):
    preserved_url = get_next_url(request)
    if preserved_url:
        url = f"{preserved_url}"
        del request.session['preserved_url']
        return redirect(str(url))
    return None


def set_logged_in_user(request, userid):
    request.session['logged_in_user'] = userid


def get_logged_in_user(request):
    return request.session.get('logged_in_user', None)


def remove_message(request, message_text=None, remove_all=False):
    if request is not None:
        storage = messages.get_messages(request)
        if storage is not None:
            if remove_all:
                storage._queued_messages = []
                storage._loaded_data = []
            elif message_text is not None:
                if message_text in storage._queued_messages:
                    storage._queued_messages.remove(message_text)
                if message_text in storage._loaded_data:
                    storage._loaded_data.remove(message_text)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def validate_login(request=None, email=None):
    if request is None:
        raise utils.product_exception.ProductException(request=request,
                                                       message=f'User cannot be validated.'
                                                               f'\nReason: Request is obtained as null',
                                                       custom_message=f'User cannot be validated.'
                                                                      f'\nReason: Request is obtained as null',
                                                       mode='redirect', page='userauths:sign-in',
                                                       logoff=True)
    if email is None:
        raise utils.product_exception.ProductException(request=request,
                                                       message=f'User cannot be validated.'
                                                               f'\nReason: Email is obtained as null',
                                                       custom_message=f'User cannot be validated.'
                                                                      f'\nReason: Email is obtained as null',
                                                       mode='redirect', page='userauths:sign-in',
                                                       logoff=True)

    required_signin = False
    if check_session_timeout(request):
        set_next_url(request)
        required_signin = True
    elif not request.user.is_authenticated:
        required_signin = True
    if required_signin:
        return redirect('userauths:sign-in')

    if utils.encrypt_decrypt.EncryptDecrypt().decrypt_parameter(
            encrypted_parameter=get_logged_in_user(request)) != utils.encrypt_decrypt.EncryptDecrypt(). \
            decrypt_parameter(encrypted_parameter=email):
        raise utils.product_exception.ProductException(request=request,
                                                       message=f'Permission denied. Please log in with proper credentials.',
                                                       custom_message=f'Permission denied. Please log in with proper credentials.',
                                                       mode='redirect', page='userauths:sign-in',
                                                       logoff=True)
