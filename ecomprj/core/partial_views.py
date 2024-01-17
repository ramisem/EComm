from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.template.loader import render_to_string

from core.db.service.category_service import CategoryService
from utils.logger import print_log
from utils.product_exception import ProductException


def get_all_categories_by_pagination(request):
    try:
        print_log.info(message='get_all_categories_pagination partial view is getting called')
        category_list = CategoryService(service_name='get_category_list', filters={'all': True}).execute_service()
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 5)
        logged_in_emailid = request.GET.get('logged_in_emailid', None);
        paginator = Paginator(category_list, page_size)
        try:
            # Get the requested page
            final_category_list = paginator.page(page)
        except EmptyPage:
            return JsonResponse({'categories_html': ''})

        categories_html = render_to_string('partials/category_dropdown.html',
                                           {'categories': final_category_list, 'email': logged_in_emailid})

        return JsonResponse({'categories_html': categories_html})

    except Exception as exp:
        try:
            raise ProductException(request=request,
                                   message=f'Exception occurred from the get_all_categories_pagination partial view.'
                                           f'\nPlease check log for more details',
                                   custom_message=f'Exception occurred from the get_all_categories_pagination '
                                                  f'partial view.nPlease check log for more details.',
                                   logoff=False, jsonresponse=True, no_ui_message=True)
        except ProductException as pexp:
            return pexp.handle_exception()
    finally:
        print_log.info(message='get_all_categories_pagination partial view call ends')
