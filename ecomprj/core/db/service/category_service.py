from core.db.service.service import Service
from core.models import Category
from django.db.models import Count,Q


class CategoryService(Service):
    def __init__(self, service_name=None, filters=None):
        self.service_name = service_name
        self.filters = filters or {}

    # Example of filters dictionary for this service: {all:True,col1:[],col2[], condition='OR'}
    def get_category_list(self):
        if self.filters is not None and self.filters and len(self.filters) > 0:
            category_id = self.filters.get('id', None)
            if category_id is not None:
                return Category.objects.filter(id=category_id).annotate(item_count=Count("product_category"))
            if 'all' in self.filters and isinstance(self.filters['all'], bool) and self.filters['all']:
                return Category.objects.all().annotate(item_count=Count("product_category"))
            query = Q()
            for key, value_list in self.filters.items():
                if key.lower() in ('all', 'condition'):
                    continue

                if self.filters['condition'] == 'OR':
                    query |= Q(**{f"{key}__in": value_list})
                elif self.filters['condition'] == 'AND' or 'condition' not in self.filters:
                    query &= Q(**{f"{key}__in": value_list})
            return Category.objects.filter(query).annotate(item_count=Count("product_category"))
        else:
            return None
