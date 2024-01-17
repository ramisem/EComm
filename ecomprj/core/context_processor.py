from core.db.service.category_service import CategoryService
from utils.logger import print_log
from utils.product_exception import ProductException
from django.core.paginator import Paginator


def get_all_categories(request):
    try:
        print_log.info(message='get_all_categories contex processor is getting called')
        category_list = CategoryService(service_name='get_category_list', filters={'all': True}).execute_service()
        context = {'all_categories': category_list}
        return context
    except ProductException as pexp:
        pexp.set_request(request=request)
        return pexp.handle_exception()
    except Exception as exp:
        try:
            raise ProductException(request=request,
                                   message=f'Exception occurred from the contex processor get_all_categories.'
                                           f'\nPlease check log for more details',
                                   custom_message=f'Exception occurred from the contex processor '
                                                  f'get_all_categories.'
                                                  f'\nPlease check log for more details',
                                   mode='redirect', page='userauths:sign-in',
                                   logoff=True)
        except ProductException as pexp:
            pexp.set_request(request=request)
            return pexp.handle_exception()
    finally:
        print_log.info(message='get_all_categories contex processor call ends')



