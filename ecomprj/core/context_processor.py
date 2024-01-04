from core.db.service.category_service import CategoryService


def get_all_categories_base_html(request):
    category_list = CategoryService(service_name='get_category_list', filters={'all': True}).execute_service()
    context = {'base_categories': category_list}
    return context
