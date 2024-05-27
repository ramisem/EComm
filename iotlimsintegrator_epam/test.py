import json


def evaluate_event_rule_condition(response, event_rule_info, event_rule_param_info):
    data_list = response.json()
    data = data_list[0]
    result = []
    for each_param_spec_condition in event_rule_param_info:
        result_for_each_param = each_param_spec_condition.execute_event_rule_condition_evaluation(data)
        result.append(result_for_each_param)
    return json.dumps(result)
