import json
from utils.product_exception import ProductException
from django.http import JsonResponse


# The below view assumes the json_data to have the dictionary object in the below format
# input_dict_obj = {
#     "method1": {"package": "my_package", "method_name": "method1", "params": ("value1")},
#     "method2": {"package": "my_package", "method_name": "method2", "params": ("value1", "value2")}
# }

def command(request):
    try:
        if request.method == 'POST':
            input_dict_obj = request.POST.get('data')
            if input_dict_obj is not None:
                input_dict_obj_list = json.loads(input_dict_obj)
                if input_dict_obj_list is not None:
                    # Iterate over each set in the list
                    results = []
                    for method_info in input_dict_obj_list:
                        package_name = method_info.get("package_name")
                        method_name = method_info.get("method_name")
                        params = method_info.get('params', [])
                        params.insert(0, request)

                        if package_name and method_name:
                            try:
                                full_module_path = f"{package_name}"
                                module = __import__(full_module_path, fromlist=['method_name'])
                                if hasattr(module, method_name):
                                    method_to_execute = getattr(module, method_name)
                                    result = method_to_execute(*params)
                                    results.append({'result': result})
                                else:
                                    raise ProductException(request=request,
                                                           message=f"Method '{method_name}' does not exist in the "
                                                                   f"module '{full_module_path}'.",
                                                           custom_message=f"Method '{method_name}' does not exist  "
                                                                          f"in the module '{full_module_path}'.",
                                                           logoff=False, jsonresponse=True)

                            except ImportError:
                                raise ProductException(request=request,
                                                       message=f"Module '{package_name}' not found.",
                                                       custom_message=f"Module '{package_name}' not found.",
                                                       logoff=False, jsonresponse=True)
                            except AttributeError:
                                raise ProductException(request=request,
                                                       message=f"Method '{method_name}' does not exist "
                                                               f"in module '{package_name}'.",
                                                       custom_message=f"Method '{method_name}' does not exist "
                                                                      f"in module '{package_name}'.",
                                                       logoff=False, jsonresponse=True)
                        else:
                            raise ProductException(request=request,
                                                   message="Invalid method information in the dictionary.",
                                                   custom_message="Invalid method information in the dictionary.",
                                                   logoff=False, jsonresponse=True)

                    return JsonResponse({'results': results})

                else:
                    raise ProductException(request=request,
                                           message="input_dict_obj_list is None.",
                                           custom_message="input_dict_obj_list is None.",
                                           logoff=False, jsonresponse=True)
            else:
                raise ProductException(request=request,
                                       message="input_dict_obj is None.",
                                       custom_message="input_dict_obj is None.",
                                       logoff=False, jsonresponse=True)
        else:
            raise ProductException(request=request,
                                   message="POST request type is not obtained",
                                   custom_message="POST request type is not obtained",
                                   logoff=False, jsonresponse=True)

    except ProductException as pexp:
        return pexp.handle_exception()
