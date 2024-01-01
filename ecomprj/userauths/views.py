from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from userauths.models import User
from utils.util import *
from utils.encrypt_decrypt import *
from django.shortcuts import render
from django.contrib.messages import info


def register_view(request):
    print_log.info(message='register_view is getting called')
    error_occurred = False
    success_msg = None
    try:
        form = UserRegisterForm()

        context = {
            'form': form,
        }
        if request.method == 'POST':
            form = UserRegisterForm(request.POST or None)
            if form.is_valid():
                form.save()
                user_name = form.cleaned_data.get('username')
                print_log.info(message=f'{user_name}, account is successfully created')
                success_msg = f'Hey {user_name}, Your account is successfully created'
                new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
                login(request, new_user)
                print_log.info(message=f'User {user_name}, is successfully logged in.')
                encrypted_email_id = EncryptDecrypt().encrypt_parameter(parameter=form.cleaned_data['email'])
                set_logged_in_user(request, encrypted_email_id)
                return redirect('core:index',
                                email=encrypted_email_id)
            else:
                raise ProductException(request=request,
                                       message=f'Exception occurred from the view register_view. '
                                               f'Please check log for more details',
                                       custom_message=f'Exception occurred from the view register_view. '
                                                      f'Please check log for more details',
                                       mode='redirect', page='userauths:sign-in',
                                       context=context, logoff=True)

        else:
            print_log.info(message=f'POST request didn\'t received for the view register_view')
            return render(request, 'userauths/sign-up.html', context)

    except ProductException as pexp:
        error_occurred = True
        return pexp.handle_exception()
    except Exception as exp:
        error_occurred = True
        try:
            raise ProductException(request=request,
                                   message=f'Exception occurred from the view register_view. '
                                           f'Please check log for more details',
                                   custom_message=f'Exception occurred from the view register_view. '
                                                  f'Please check log for more details',
                                   mode='redirect', page='userauths:sign-in',
                                   context=context, logoff=True)
        except ProductException as pexp:
            return pexp.handle_exception()
    finally:
        if not error_occurred and success_msg is not None:
            messages.success(request, success_msg)
        print_log.info(message='register_view call is end here')


def login_view(request):
    print_log.info(message='login_view is getting called')
    error_occurred = False
    success_msg = None

    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            if request.user.is_authenticated:
                success_msg = 'Hey, you are already logged in'
                print_log.info(message=f'User {email}, is already logged in.')
                return redirect('core:index', email=EncryptDecrypt().encrypt_parameter(parameter=email))
            elif request.method == 'POST':
                password = request.POST.get('password')
                try:
                    User.objects.get(email=email)
                    print_log.info(message=f'User {email}, got validated successfully.')
                except Exception as exp:
                    raise ProductException(request=request, message=f'User with email-id {email} doesn\'t exist',
                                           custom_message=f'User with email-id {email} doesn\'t exist',
                                           mode='redirect', page='userauths:sign-in',
                                           context={'email': None})

                user = authenticate(request, email=email, password=password)

                if user is not None:
                    print_log.info(
                        message=f'User {email}, got authenticated successfully and obtained the user object.')
                    login(request, user)
                    print_log.info(
                        message=f'User {email}, got logged in successfully..')
                    success_msg = f'User with email-id {email} has logged in successfully'

                    encrypted_email_id = EncryptDecrypt().encrypt_parameter(parameter=email)
                    set_logged_in_user(request, encrypted_email_id)

                    redirect_obj = redirect_to_next_url(request)

                    if redirect_obj is not None:
                        return redirect_obj
                    else:
                        return redirect('core:index', email=encrypted_email_id)
                else:
                    raise ProductException(request=request, message='Invalid user-id/password',
                                           custom_message='Invalid user-id/password',
                                           mode='redirect', page='userauths:sign-in',
                                           context={'email': None}, logoff=True)
        else:
            print_log.info(message=f'POST request didn\'t receive for the view login_view')
            return render(request, 'userauths/sign-in.html', {'email': None})

    except ProductException as pexp:
        error_occurred = True
        return pexp.handle_exception()
    except Exception as exp:
        error_occurred = True
        try:
            context = {
                'email': None
            }
            raise ProductException(request=request,
                                   message=f'Exception occurred from the view login_view. '
                                           f'Please check log for more details',
                                   custom_message=f'Exception occurred from the view login_view. '
                                                  f'Please check log for more details',
                                   mode='redirect', page='userauths:sign-in',
                                   context=context, logoff=True)
        except ProductException as pexp:
            return pexp.handle_exception()
    finally:
        if not error_occurred and success_msg is not None:
            messages.success(request, success_msg)
        print_log.info(message='login_view call is end here')


def logout_view(request):
    print_log.info(message='logout_view is getting called')
    error_occurred = False
    success_msg = None
    autoredirect = request.GET.get('autoredirect', None)
    try:
        if autoredirect is not None and autoredirect.lower() == 'y':
            if hasattr(settings, 'AUTO_LOGOUT'):
                auto_logout_prop = settings.AUTO_LOGOUT
                if 'MESSAGE' in auto_logout_prop:
                    info(request, auto_logout_prop['MESSAGE'])
        logout(request)
        print_log.info(message='Log-out operation is successful')
        success_msg = f'You have logged out successfully.'
        return redirect('userauths:sign-in')
    except Exception as exp:
        error_occurred = True
        try:
            context = {
                'email': None
            }
            raise ProductException(request=request,
                                   message=f'Exception occurred from the view logout_view. '
                                           f'Please check log for more details',
                                   custom_message=f'Exception occurred from the view logout_view. '
                                                  f'Please check log for more details',
                                   mode='redirect', page='core:index',
                                   context=context)
        except ProductException as pexp:
            return pexp.handle_exception()
    finally:
        if not error_occurred and success_msg is not None:
            messages.success(request, success_msg)
        print_log.info(message='logout_view call is end here')


def logout_view_with_param(request, email):
    print_log.info(message='logout_view_with_param is getting called')
    error_occurred = False
    success_msg = None
    autoredirect = request.GET.get('autoredirect', None)
    try:
        org_email = None
        if email is not None:
            org_email = EncryptDecrypt().decrypt_parameter(encrypted_parameter=email)

        if autoredirect is not None and autoredirect.lower() == 'y':
            if hasattr(settings, 'AUTO_LOGOUT'):
                auto_logout_prop = settings.AUTO_LOGOUT
                if 'MESSAGE' in auto_logout_prop:
                    info(request, auto_logout_prop['MESSAGE'])

        logout(request)
        if email is not None and org_email is not None:
            print_log.info(message=f'Log-out operation is successful for the user {org_email}.')
            success_msg = f'User with email-id {org_email} has logged out successfully.'
        else:
            print_log.info(message=f'Current user is successfully logged out.')
            success_msg = f'Current user is successfully logged out.'
        return redirect('userauths:sign-in')
    except Exception as exp:
        error_occurred = True
        try:
            context = {
                'email': email
            }
            raise ProductException(request=request,
                                   message=f'Exception occurred from the view logout_view. '
                                           f'Please check log for more details',
                                   custom_message=f'Exception occurred from the view logout_view. '
                                                  f'Please check log for more details',
                                   mode='redirect', page='core:index',
                                   context=context)
        except ProductException as pexp:
            return pexp.handle_exception()
    finally:
        if not error_occurred and success_msg is not None:
            messages.success(request, success_msg)
        print_log.info(message='logout_view_with_param call is end here')
