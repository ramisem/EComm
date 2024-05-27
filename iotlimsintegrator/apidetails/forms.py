import ast

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from apidetails.models import API_Property_Details, APIDetail


class API_Detail_Form(forms.ModelForm):
    class Meta:
        model = APIDetail
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        api_type = cleaned_data.get('type', '')
        app_id = cleaned_data.get('app_id', '')
        processing_script = cleaned_data.get('processing_script', '')

        is_valid, error = self.check_syntactical_error(processing_script)
        if not is_valid:
            raise ValidationError(f"Syntax error occurred: {error}")

        if api_type == 'connection':
            count = APIDetail.objects.filter(app_id__app_detail_id=app_id.app_detail_id, type='connection').count()
            if count > 0:
                raise ValidationError(f"One connection api already exists for this application.")
            is_valid, error = self.check_syntax(processing_script, getattr(settings,
                                                                           'APPLICATION_TASK_HANDLER_PROCESS_FOR_LIMS_CONNECTION'),
                                                1)
            if not is_valid:
                raise ValidationError(f"Syntax error occurred: {error}")
        elif api_type == 'outbound':
            is_valid, error = self.check_syntax(processing_script,
                                                getattr(settings, 'APPLICATION_TASK_HANDLER_PROCESS_FOR_LIMS'), 2)
            if not is_valid:
                raise ValidationError(f"Syntax error occurred: {error}")
        elif api_type == 'inbound':
            is_valid, error = self.check_syntax(processing_script,
                                                getattr(settings, 'APPLICATION_TASK_HANDLER_PROCESS_FOR_EM'), 3)
            if not is_valid:
                raise ValidationError(f"Syntax error occurred: {error}")

        return cleaned_data

    def check_syntactical_error(self, script):
        try:
            compile(script, "<string>", "exec")
            return True, None  # No syntax errors
        except SyntaxError as e:
            return False, e  # Syntax error occurred

    def check_syntax(self, script, function_name, no_arguments):
        try:
            tree = ast.parse(script)
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    # Check method name and arguments
                    if node.name != function_name:
                        raise SyntaxError(f"Method name should be {function_name}, found '{node.name}'")
                    if len(node.args.args) != no_arguments:
                        raise SyntaxError(f"Method {function_name} should have exactly {no_arguments} arguments")
                    function_body = ast.get_source_segment(script, node.body[0])
                    try:
                        compile(function_body, "<string>", "exec")
                    except SyntaxError as e:
                        return False, e  # Syntax error in function body
            return True, None  # No syntax errors
        except SyntaxError as e:
            return False, e  # Syntax error occurred


class API_Property_Details_Form(forms.ModelForm):
    class Meta:
        model = API_Property_Details
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        property_value = cleaned_data.get('property_value', '')
        is_keyword = cleaned_data.get('is_keyword', '')

        # Perform your validation logic here
        if (property_value is None or property_value == '') and (is_keyword is None or is_keyword == ''):
            raise ValidationError("Please provide either Property Value or mark it as keyword")
        elif property_value is not None and property_value != '' and is_keyword is not None and is_keyword != '':
            raise ValidationError(
                "Please provide the value to either Property Value or mark it as keyword. Don't provide the values for both the columns.")

        # Return cleaned data
        return cleaned_data
