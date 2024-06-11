from django import template
from django.conf import settings

from refenrencetype.models import RefValues

register = template.Library()


@register.simple_tag
def get_module_images():
    required_reftype_id = getattr(settings, 'APPLICATION_MODULE_IMAGES_REF_NO', '-1')
    module_images = RefValues.objects.filter(reftype_id=int(required_reftype_id)).values_list('value',
                                                                                              'display_value')
    module_images_dict = {value: display_value for value, display_value in module_images}
    return module_images_dict
