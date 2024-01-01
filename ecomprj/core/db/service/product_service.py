from core.db.service.service import Service
from core.models import Product, ProductReview, ProductImages
from django.db.models import Q
from utils.product_exception import ProductException


class ProductService(Service):

    def __init__(self, service_name=None, filters=None, request=None):
        self.service_name = service_name
        self.filters = filters or {}
        self.request = request

    # Example of filters dictionary for this service: {all:True,col1:[],col2[], condition='OR'}
    def get_product_list(self):
        if self.filters is not None and self.filters and len(self.filters) > 0:
            product_id = self.filters.get('id', None)
            if product_id is not None:
                return Product.objects.filter(id=product_id)
            if 'all' in self.filters and isinstance(self.filters['all'], bool) and self.filters['all']:
                return Product.objects.all()
            query = Q()
            for key, value_list in self.filters.items():
                if key.lower() in ('all', 'condition'):
                    continue

                if self.filters['condition'] == 'OR':
                    query |= Q(**{f"{key}__in": value_list})
                elif self.filters['condition'] == 'AND' or 'condition' not in self.filters:
                    query &= Q(**{f"{key}__in": value_list})
            return Product.objects.filter(query)
        else:
            return None

    # Example of filters dictionary for this service: {all:True,col1:[],col2[], condition='OR'}
    def get_product_images_list(self):
        if self.filters is not None and self.filters and len(self.filters) > 0:
            if 'all' in self.filters and isinstance(self.filters['all'], bool) and self.filters['all']:
                raise ProductException(request=self.request,
                                       message=f'Exception occurred from get_product_images_list method. '
                                               f'\nReason:Cannot show the images for all the products together. '
                                               f'Please provide specific product ids.',
                                       custom_message=f'Exception occurred from get_product_images_list method. '
                                               f'\nReason:Cannot show the images for all the products together. '
                                               f'Please provide specific product ids.',
                                       logoff=False)
            query = Q()
            for key, value_list in self.filters.items():
                if key.lower() in ('all', 'condition'):
                    continue

                if self.filters['condition'] == 'OR':
                    query |= Q(**{f"{key}__in": value_list})
                elif self.filters['condition'] == 'AND' or 'condition' not in self.filters:
                    query &= Q(**{f"{key}__in": value_list})
            return Product.objects.filter(query)
        else:
            return None
