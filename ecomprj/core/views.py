from django.shortcuts import render
from utils.util import *
from utils.encrypt_decrypt import *
from utils.product_exception import ProductException
from django_auto_logout.utils import now, seconds_until_idle_time_end
from core.db.service.product_service import ProductService
from core.db.service.category_service import CategoryService


# Create your views here.

def index(request, email):
    try:
        print_log.info(message='index view is getting called')
        validate_login(request=request, email=email)
        context = {'email': email}
        if hasattr(settings, 'AUTO_LOGOUT') and 'IDLE_TIME' in settings.AUTO_LOGOUT:
            context.update(
                {'idle_time': seconds_until_idle_time_end(request, settings.AUTO_LOGOUT['IDLE_TIME'], now())})

        product_list = ProductService(service_name='get_product_list', filters={'all': True}).execute_service()

        if product_list is None:
            raise ProductException(request=request,
                                   message=f'Product list cannot be obtained',
                                   custom_message=f'Product list cannot be obtained',
                                   mode='redirect', page='userauths:sign-in',
                                   logoff=True)
        context.update({'product_list': product_list})

        return render(request, 'core/index.html', context)

    except ProductException as pexp:
        pexp.set_request(request=request)
        return pexp.handle_exception()
    except Exception as exp:
        try:
            raise ProductException(request=request,
                                   message=f'Exception occurred from the view index. '
                                           f'Please check log for more details',
                                   custom_message=f'Exception occurred from the view index. '
                                                  f'Please check log for more details',
                                   mode='redirect', page='userauths:sign-in',
                                   logoff=True)
        except ProductException as pexp:
            pexp.set_request(request=request)
            return pexp.handle_exception()
    finally:
        print_log.info(message='index view call ends')


def home_page_view(request):
    try:
        if request.user.is_authenticated:
            messages.success(request,
                             'There is another active connection obtained. '
                             'Please login again to validate your credential')
            return redirect('userauths:sign-in')
        else:
            print_log.info(message='home_page_view view is getting called')
            return render(request, 'core/index.html', {'email': None})
    finally:
        print_log.info(message='home_page_view view call ends')


def category_list_view(request, email=None):
    try:
        print_log.info(message='category_list_view view is getting called')
        if email is not None:
            validate_login(request=request, email=email)
        else:
            print_log.info(message='validate_login has been skipped as email id is obtained as None.')
        category_list = CategoryService(service_name='get_category_list', filters={'all': True}).execute_service()
        context = {'category_list': category_list, 'email': email}
        if hasattr(settings, 'AUTO_LOGOUT') and 'IDLE_TIME' in settings.AUTO_LOGOUT:
            context.update(
                {'idle_time': seconds_until_idle_time_end(request, settings.AUTO_LOGOUT['IDLE_TIME'], now())})
        return render(request, 'core/categorylist.html', context)

    except ProductException as pexp:
        pexp.set_request(request=request)
        return pexp.handle_exception()
    except Exception as exp:
        try:
            raise ProductException(request=request,
                                   message=f'Exception occurred from the view category_list_view. '
                                           f'Please check log for more details',
                                   custom_message=f'Exception occurred from the view category_list_view. '
                                                  f'Please check log for more details',
                                   mode='redirect', page='userauths:sign-in',
                                   logoff=True)
        except ProductException as pexp:
            pexp.set_request(request=request)
            return pexp.handle_exception()
    finally:
        print_log.info(message='category_list_view view call ends')


def product_list_by_category_view(request, email=None):
    try:
        print_log.info(message='product_list_by_category_view view is getting called')
        if email is not None:
            validate_login(request=request, email=email)
        else:
            print_log.info(message='validate_login has been skipped as email id is obtained as None.')

        category_id = request.GET.get('categoryid', None)

        if category_id is None:
            raise ProductException(request=request,
                                   message=f'Exception occurred from the view product_list_by_category_view. '
                                           f'\nReason:Category Id is not obtained',
                                   custom_message=f'Exception occurred from the view product_list_by_category_view. '
                                                  f'\nReason:Category Id is not obtained',
                                   mode='redirect', page='userauths:sign-in',
                                   logoff=True)

        product_list = ProductService(service_name='get_product_list',
                                      filters={'category': category_id,
                                               'condition': 'AND'}).execute_service()
        category = CategoryService(service_name='get_category_list',
                                   filters={'id': category_id,
                                            'condition': 'AND'}).execute_service()
        context = {'products': product_list, 'category': category[0], 'email': email}
        if hasattr(settings, 'AUTO_LOGOUT') and 'IDLE_TIME' in settings.AUTO_LOGOUT:
            context.update(
                {'idle_time': seconds_until_idle_time_end(request, settings.AUTO_LOGOUT['IDLE_TIME'], now())})
        return render(request, 'core/category_productlist.html', context)

    except ProductException as pexp:
        pexp.set_request(request=request)
        return pexp.handle_exception()
    except Exception as exp:
        try:
            raise ProductException(request=request,
                                   message=f'Exception occurred from the view product_list_by_category_view. '
                                           f'Please check log for more details',
                                   custom_message=f'Exception occurred from the view product_list_by_category_view. '
                                                  f'Please check log for more details',
                                   mode='redirect', page='userauths:sign-in',
                                   logoff=True)
        except ProductException as pexp:
            pexp.set_request(request=request)
            return pexp.handle_exception()
    finally:
        print_log.info(message='product_list_by_category_view view call ends')


def product_details_view(request, email=None):
    try:
        print_log.info(message='product_details_view view is getting called')
        if email is not None:
            validate_login(request=request, email=email)
        else:
            print_log.info(message='validate_login has been skipped as email id is obtained as None.')

        productid = request.GET.get('productid', None)

        if productid is None:
            raise ProductException(request=request,
                                   message=f'Exception occurred from the view product_list_by_category_view. '
                                           f'\nReason:Product Id is not obtained',
                                   custom_message=f'Exception occurred from the view product_list_by_category_view. '
                                                  f'\nReason:Product Id is not obtained',
                                   mode='redirect', page='userauths:sign-in',
                                   logoff=True)

        product_details = ProductService(service_name='get_product_list',
                                         filters={'pid': productid,
                                                  'condition': 'AND'}).execute_service()
        p_image = ProductService(service_name='get_product_images_list',
                                 filters={'product': productid.id,
                                          'condition': 'AND'}, request=request).execute_service()
        context = {'p': product_details, 'p_image': p_image, 'email': email}
        if hasattr(settings, 'AUTO_LOGOUT') and 'IDLE_TIME' in settings.AUTO_LOGOUT:
            context.update(
                {'idle_time': seconds_until_idle_time_end(request, settings.AUTO_LOGOUT['IDLE_TIME'], now())})
        return render(request, 'core/product_details.html', context)

    except ProductException as pexp:
        pexp.set_request(request=request)
        return pexp.handle_exception()
    except Exception as exp:
        try:
            raise ProductException(request=request,
                                   message=f'Exception occurred from the view product_details_view. '
                                           f'Please check log for more details',
                                   custom_message=f'Exception occurred from the view product_details_view. '
                                                  f'Please check log for more details',
                                   mode='redirect', page='userauths:sign-in',
                                   logoff=True)
        except ProductException as pexp:
            pexp.set_request(request=request)
            return pexp.handle_exception()
    finally:
        print_log.info(message='product_details_view view call ends')


def product_vendor_details_view(request, email=None):
    pass


def product_tags_details_view(request, email=None):
    pass
