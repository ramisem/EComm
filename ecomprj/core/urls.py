from django.urls import path
from core.views import index, home_page_view, category_list_view, product_list_by_category_view, product_details_view, \
    product_vendor_details_view,product_tags_details_view

app_name = 'core'


class URLS:
    urlpatterns = [
        path('<str:email>/', index, name='index'),
        path('', home_page_view, name='homepage'),
        path('category/categorylist/', category_list_view, name='categorylist'),
        path('category/categorylist/<str:email>/', category_list_view, name='categorylist'),
        path('category/product/', product_list_by_category_view, name='product_list_by_category'),
        path('category/product/<str:email>/', product_list_by_category_view, name='product_list_by_category'),
        path('product/productdetails/', product_details_view, name='product-detail'),
        path('product/productdetails/<str:email>/', product_details_view, name='product-detail'),
        path('product/vendordetails/', product_vendor_details_view, name='vendor-detail'),
        path('product/vendordetails/<str:email>/', product_vendor_details_view, name='vendor-detail'),
        path('product/tags/', product_tags_details_view, name='tags'),
        path('product/tags/<str:email>/', product_tags_details_view, name='tags'),
    ]

    def __dir__(self):
        return URLS.urlpatterns
