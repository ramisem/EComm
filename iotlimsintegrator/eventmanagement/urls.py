from django.urls import path

from eventmanagement import views

app_name = 'eventmanagement'


class URLS:
    urlpatterns = [
        path('ajax/get_iot_types_by_event_type/', views.get_iot_types_by_event_type,
             name='ajax_get_iot_types_by_event_type'),
        path('ajax/get_paramid_by_event_type_iot_type_map_id/', views.get_paramid_by_event_type_iot_type_map_id,
             name='get_paramid_by_event_type_iot_type_map_id'),
        path('ajax/get_param_unit_by_param_id/', views.get_param_unit_by_param_id,
             name='get_param_unit_by_param_id'),
        path('ajax/get_param_unit_by_multiple_param_ids/', views.get_param_unit_by_multiple_param_ids,
             name='get_param_unit_by_multiple_param_ids'),
    ]

    def __dir__(self):
        return self.urlpatterns
