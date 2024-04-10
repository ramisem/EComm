from django.http import JsonResponse

import core.models
from masterdata.models import Event_Type_IOT_Type_Map, EventRuleParams, Param


def get_iot_types_by_event_type(request):
    event_type_id = request.GET.get('event_type_id', None)
    if event_type_id is not None:
        iot_types_ids = Event_Type_IOT_Type_Map.objects.filter(event_type_id=event_type_id).values('iot_type_id')
        iot_types = core.models.IOT_Type.objects.filter(iot_type_id__in=iot_types_ids).values('iot_type_id',
                                                                                              'model_name')
        return JsonResponse(list(iot_types), safe=False)
    else:
        return JsonResponse({'error': 'Missing event_type_id'}, status=400)


def get_paramid_by_event_type_iot_type_map_id(request):
    event_type_iot_type_map_id = request.GET.get('event_type_iot_type_map_id', None)
    if event_type_iot_type_map_id is not None:
        param_ids = EventRuleParams.objects.filter(event_type_iot_map_id=event_type_iot_type_map_id).values('paramid')
        param_info = Param.objects.filter(param_id__in=param_ids).values('param_id', 'param_name')
        return JsonResponse(list(param_info), safe=False)
    else:
        return JsonResponse({'error': 'Missing event_type_iot_type_map_id'}, status=400)


def get_param_unit_by_param_id(request):
    param_id = request.GET.get('param_id', None)
    if param_id is not None:
        param = Param.objects.get(param_id=param_id)
        unit_name = param.unit.unit_name if param.unit else None
        return JsonResponse(unit_name, safe=False)
    else:
        return JsonResponse({'error': 'Missing param_id'}, status=400)


def get_param_unit_by_multiple_param_ids(request):
    param_ids = request.GET.get('param_ids', None)
    if param_ids is not None:
        param_id_list = param_ids.split(',')
        params_info = Param.objects.filter(param_id__in=param_id_list).values_list('param_id', 'unit__unit_name')
        return JsonResponse(list(params_info), safe=False)
    else:
        return JsonResponse({'error': 'Missing param_ids'}, status=400)
