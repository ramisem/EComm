import json
import pickle
import re

import requests
from celery import shared_task
from django.conf import settings
from django.db.models import F
from requests.exceptions import InvalidJSONError

from apidetails.models import APIDetail, API_Property_Details
from core.models import IOT_Device
from eventmanagement.models import Event_Rule, Event_Rule_Params
from iotlimsintegrator.celery import app
from task.models import TaskAudit


@shared_task(bind=True, track_started=True)
def task_handler(self, param1, param2):
    event_rule_id = self.request.args[0]
    periodic_task_id = self.request.args[1]
    if event_rule_id is None:
        raise Exception(f"Error: Event_Rule Id does not exist.")

    try:
        event_rule_info = Event_Rule.objects.select_related('iot_type_id', 'inbound_api', 'outbound_api').get(
            pk=event_rule_id)
    except Event_Rule.DoesNotExist:
        raise Exception(f"Error: Event_Rule with ID {event_rule_id} does not exist.")

    try:
        event_rule_param_info = Event_Rule_Params.objects.filter(event_rule_id=event_rule_id).select_related('param_id')
    except Event_Rule_Params.DoesNotExist:
        raise Exception(f"Error: No parameter is defined  for the Event Rule ID {event_rule_id}.")

    if event_rule_info.outbound_api:
        outbound_api_details = APIDetail.objects.select_related('app_id').get(pk=event_rule_info.outbound_api_id)
        try:
            outbound_api_url_properties = outbound_api_details.api_property_details_set.filter(is_url_property='Y')
        except API_Property_Details.DoesNotExist:
            outbound_api_url_properties = None

        try:
            outbound_api_properties = outbound_api_details.api_property_details_set.exclude(is_url_property='Y')
        except API_Property_Details.DoesNotExist:
            outbound_api_properties = None

        try:
            connection_api_details_for_outbound_api_call = APIDetail.objects.filter(
                app_id__app_detail_id=outbound_api_details.app_id.app_detail_id, type='connection')
        except APIDetail.DoesNotExist:
            connection_api_details_for_outbound_api_call = None

        if connection_api_details_for_outbound_api_call is not None:
            try:
                connection_api_url_properties_for_outbound_api_call = API_Property_Details.objects.filter(
                    api_detail_id__in=connection_api_details_for_outbound_api_call, is_url_property='Y'
                )
            except API_Property_Details.DoesNotExist:
                connection_api_url_properties_for_outbound_api_call = None

            try:
                connection_api_properties_for_outbound_api_call = API_Property_Details.objects.filter(
                    api_detail_id__in=connection_api_details_for_outbound_api_call
                ).exclude(is_url_property='Y')
            except API_Property_Details.DoesNotExist:
                connection_api_properties_for_outbound_api_call = None

    if event_rule_info.inbound_api:
        inbound_api_details = APIDetail.objects.select_related('app_id').get(pk=event_rule_info.inbound_api_id)
        try:
            inbound_api_url_properties = inbound_api_details.api_property_details_set.filter(is_url_property='Y')
        except API_Property_Details.DoesNotExist:
            inbound_api_url_properties = None

    if event_rule_info.iot_type_id:
        try:
            iot_device_info = IOT_Device.objects.filter(
                iot_type_id=event_rule_info.iot_type_id.iot_type_id).select_related(
                'iot_type_id')
            for individual_iot_device in iot_device_info:
                process_task.delay(periodic_task_id, self.request.id, serialize_object(individual_iot_device),
                                   serialize_object(event_rule_info),
                                   serialize_object(event_rule_param_info), serialize_object(inbound_api_details),
                                   serialize_object(outbound_api_details), serialize_object(inbound_api_url_properties),
                                   serialize_object(outbound_api_url_properties),
                                   serialize_object(outbound_api_properties),
                                   serialize_object(connection_api_details_for_outbound_api_call),
                                   serialize_object(connection_api_url_properties_for_outbound_api_call),
                                   serialize_object(connection_api_properties_for_outbound_api_call))
        except IOT_Device.DoesNotExist:
            raise Exception(
                f"Error: No IOT device is registered for the IOT Type {event_rule_info.iot_type_id.model_name}.")

    return f"Execution of the task {self.request.id} is completed."


def serialize_object(obj):
    if obj is None:
        return None
    return pickle.dumps(obj)


def deserialize_object(serialized_obj):
    if serialized_obj is None:
        return None
    return pickle.loads(serialized_obj)


@app.task
def process_task(periodic_task_id, task_id, iot_device_obj_serialized, event_rule_info_serialized,
                 event_rule_param_info_serialized, inbound_api_details_serialized, outbound_api_details_serialized,
                 inbound_api_url_properties_serialized, outbound_api_url_properties_serialized,
                 outbound_api_properties_serialized,
                 connection_api_details_for_outbound_api_call_serialized,
                 connection_api_url_properties_for_outbound_api_call_serialized,
                 connection_api_properties_for_outbound_api_call_serialized):
    iot_device_obj = deserialize_object(iot_device_obj_serialized)
    event_rule_info = deserialize_object(event_rule_info_serialized)
    event_rule_param_info = deserialize_object(event_rule_param_info_serialized)
    inbound_api_details = deserialize_object(inbound_api_details_serialized)
    outbound_api_details = deserialize_object(outbound_api_details_serialized)
    inbound_api_url_properties = deserialize_object(inbound_api_url_properties_serialized)
    outbound_api_url_properties = deserialize_object(outbound_api_url_properties_serialized)
    outbound_api_properties = deserialize_object(outbound_api_properties_serialized)
    if outbound_api_properties is not None:
        outbound_api_properties = get_api_properties(iot_device_obj, outbound_api_properties)
    connection_api_details_for_outbound_api_call = deserialize_object(
        connection_api_details_for_outbound_api_call_serialized)
    connection_api_url_properties_for_outbound_api_call = deserialize_object(
        connection_api_url_properties_for_outbound_api_call_serialized)
    connection_api_properties_for_outbound_api_call = deserialize_object(
        connection_api_properties_for_outbound_api_call_serialized)
    if connection_api_properties_for_outbound_api_call is not None:
        connection_api_properties_for_outbound_api_call = get_api_properties(iot_device_obj,
                                                                             connection_api_properties_for_outbound_api_call)

    inbound_api_url = get_url(iot_device_obj, inbound_api_details, inbound_api_url_properties)
    outbound_api_url = get_url(iot_device_obj, outbound_api_details, outbound_api_url_properties)

    event_rule_evaluation_result, task_audit_id, successful_inbound_execution, execution_message = execute_in_bound_url(
        periodic_task_id,
        task_id,
        inbound_api_url,
        iot_device_obj,
        inbound_api_details,
        event_rule_info,
        event_rule_param_info)

    if not successful_inbound_execution:
        return f"Execution is completed with exception. Reason: {execution_message}."

    if connection_api_details_for_outbound_api_call is None:
        connection_id = getattr(settings, 'APPLICATION_LIMS_API_TOKEN_ID')
    else:
        connection_api_details_for_outbound_api_call = connection_api_details_for_outbound_api_call.first()

        connection_api_url_for_outbound_api_call = get_url(iot_device_obj, connection_api_details_for_outbound_api_call,
                                                           connection_api_url_properties_for_outbound_api_call)
        connection_id, successful_inbound_execution, execution_message = get_connection_id_for_out_bound_api_call(
            task_audit_id,
            connection_api_url_for_outbound_api_call,
            connection_api_details_for_outbound_api_call,
            connection_api_properties_for_outbound_api_call)
        if not successful_inbound_execution:
            return f"Execution is completed with exception. Reason: {execution_message}."

    successful_outbound_execution, execution_message = execute_out_bound_url(task_audit_id, iot_device_obj,
                                                                             connection_id,
                                                                             outbound_api_url,
                                                                             outbound_api_details,
                                                                             event_rule_evaluation_result)
    if not successful_outbound_execution:
        return f"Execution is completed with exception. Reason: {execution_message}."

    return "Execution is completed successfully."


def get_url(iot_device_obj, api_details, api_url_properties):
    base_url = api_details.app_id.base_url
    end_point = api_details.end_point_url
    final_url = base_url + end_point
    if api_url_properties is None:
        return final_url
    for api_property in api_url_properties:
        property_id = api_property.property_id
        property_value = api_property.property_value
        is_keyword = api_property.is_keyword
        if 'Y' == is_keyword:
            if '[access_token]' == property_id:
                property_value = getattr(settings, 'APPLICATION_IOT_DEVICE_INFO_API_TOKEN_ID', '')
            else:
                property_value = getattr(iot_device_obj, property_id[1:-1])
        final_url = re.sub(re.escape(property_id), property_value, final_url)
    return final_url


def get_api_properties(iot_device_obj, api_properties):
    result = {}
    for api_property in api_properties:
        property_id = api_property.property_id
        property_value = api_property.property_value
        is_keyword = api_property.is_keyword
        if 'Y' == is_keyword:
            if '[access_token]' == property_id:
                property_value = getattr(settings, 'APPLICATION_IOT_DEVICE_INFO_API_TOKEN_ID', '')
            else:
                property_value = getattr(iot_device_obj, property_id[1:-1])
        result[property_id] = property_value
    return json.dumps(result)


def execute_in_bound_url(periodic_task_id, task_id, inbound_api_url, iot_device_obj, inbound_api_details,
                         event_rule_info, event_rule_param_info):
    response = requests.get(inbound_api_url)
    try:
        api_response_text = response.json()
    except InvalidJSONError:
        if response.text is not None:
            api_response = {
                "response_text": response.text
            }
            api_response_text = json.dumps(api_response)
    defaults = {
        'task_id': task_id,
        'name': periodic_task_id,
        'uuid': iot_device_obj.uuid,
        'api_url': inbound_api_url,
        'status': response.status_code,
        'response_text': api_response_text,
        'data_consumed_by_api': len(response.content),
        'total_data_consumed': len(response.content)
    }
    new_task_audit_obj = TaskAudit.objects.create(**defaults)

    if response.status_code != inbound_api_details.success_code:
        return None, new_task_audit_obj.task_audit_id, False, 'EM API call failed.'

    code_to_execute = inbound_api_details.processing_script
    code_namespace = {
        'response': response,
        'event_rule_info': event_rule_info,
        'event_rule_param_info': event_rule_param_info,
    }
    try:
        exec(code_to_execute, code_namespace)
        evaluate_event_rule_condition_func = code_namespace[
            getattr(settings, 'APPLICATION_TASK_HANDLER_PROCESS_FOR_EM')]
        result_string = evaluate_event_rule_condition_func(response, event_rule_info, event_rule_param_info)
        TaskAudit.objects.filter(task_audit_id=new_task_audit_obj.task_audit_id).update(
            condition_evaluation=json.loads(result_string))
    except Exception as e:
        return None, new_task_audit_obj.task_audit_id, False, str(e)
    return result_string, new_task_audit_obj.task_audit_id, True, None


def get_connection_id_for_out_bound_api_call(task_audit_id, connection_api_url_for_outbound_api_call,
                                             connection_api_details_for_outbound_api_call,
                                             connection_api_properties_for_outbound_api_call):
    headers = {
        'Content-Type': 'application/json'
    }
    payload = json.loads(connection_api_properties_for_outbound_api_call)
    request_header_size = sum(len(key) + len(value) for key, value in headers.items())
    response = requests.post(connection_api_url_for_outbound_api_call, json=payload, headers=headers)

    try:
        api_response_text = response.json()
    except InvalidJSONError:
        if response.text is not None:
            api_response = {
                "response_text": response.text
            }
            api_response_text = json.dumps(api_response)

    total_data_consumed = len(json.dumps(payload)) + request_header_size + len(response.content)
    TaskAudit.objects.filter(task_audit_id=task_audit_id).update(
        lims_connection_api_url=connection_api_url_for_outbound_api_call,
        lims_connection_api_status=response.status_code,
        lims_connection_api_call_param=payload, lims_connection_api_response_text=api_response_text,
        data_consumed_by_lims_connection_api=total_data_consumed,
        total_data_consumed=F('total_data_consumed') + total_data_consumed)

    if response.status_code != connection_api_details_for_outbound_api_call.success_code:
        return None, False, 'LIMS Connection API call failed.'

    code_to_execute = connection_api_details_for_outbound_api_call.processing_script
    code_namespace = {
        'response': response,
    }
    try:
        exec(code_to_execute, code_namespace)
        get_connection_id_func = code_namespace[
            getattr(settings, 'APPLICATION_TASK_HANDLER_PROCESS_FOR_LIMS_CONNECTION')]
        connection_id = get_connection_id_func(response)
    except Exception as e:
        return None, False, str(e)
    return connection_id, True, None


def execute_out_bound_url(task_audit_id, iot_device_obj,
                          connection_id,
                          outbound_api_url,
                          outbound_api_details,
                          event_rule_evaluation_result):
    code_to_execute = outbound_api_details.processing_script
    code_namespace = {
        'iot_device_obj': iot_device_obj,
        'event_rule_evaluation_result': event_rule_evaluation_result,
    }
    exec(code_to_execute, code_namespace)
    execute_lims_api_data_processor_func = code_namespace[
        getattr(settings, 'APPLICATION_TASK_HANDLER_PROCESS_FOR_LIMS')]
    json_request_for_out_bound_api_call = execute_lims_api_data_processor_func(iot_device_obj,
                                                                               event_rule_evaluation_result)
    headers = {
        'Content-Type': 'application/json',  # Adjust content type if necessary
        f'{outbound_api_details.authorization_property_id}': f'{outbound_api_details.authorization_keyword} {connection_id}',
    }
    payload = json.loads(json_request_for_out_bound_api_call)
    request_header_size = sum(len(key) + len(value) for key, value in headers.items())
    response = requests.post(outbound_api_url, json=payload, headers=headers)
    try:
        api_response_text = response.json()
    except InvalidJSONError:
        if response.text is not None:
            api_response = {
                "response_text": response.text
            }
            api_response_text = json.dumps(api_response)

    total_data_consumed = len(json.dumps(payload)) + request_header_size + len(response.content)
    TaskAudit.objects.filter(task_audit_id=task_audit_id).update(
        lims_api_url=outbound_api_url, lims_status=response.status_code,
        lims_api_call_param=payload, lims_response_text=api_response_text,
        data_consumed_by_lims_api=total_data_consumed,
        total_data_consumed=F('total_data_consumed') + total_data_consumed)
    if response.status_code != outbound_api_details.success_code:
        return False, 'LIMS API call failed.'
    return True, ''
