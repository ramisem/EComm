from django import forms
from django.core.exceptions import ValidationError

from .models import Event_Rule, Event_Rule_Params


class EventRuleForm(forms.ModelForm):
    class Meta:
        model = Event_Rule
        fields = ['name', 'event_type_id', 'iot_type_id', 'inbound_api', 'outbound_api', 'created_by',
                  'event_iot_map_id']
        widgets = {
            'event_type_id': forms.Select(attrs={'class': 'form-control', 'onchange': 'populateIOTTypeByEventType()'}),
        }


class EventRuleParamForm(forms.ModelForm):
    value1_unit = forms.CharField(label='Unit', max_length=10, required=False,
                                  widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    value2_unit = forms.CharField(label='Unit', max_length=10, required=False,
                                  widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.param_id_id:
            self.fields['param_id'].disabled = True

    class Meta:
        model = Event_Rule_Params
        fields = ['param_id', 'operator1', 'value1', 'value1_unit', 'condition', 'operator2', 'value2', 'value2_unit',
                  'value_text']
        widgets = {
            'value1': forms.TextInput(attrs={'onchange': 'populateParamUnit(this.id)'}),
            'value2': forms.TextInput(attrs={'onchange': 'populateParamUnit(this.id)'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        operator1 = cleaned_data.get('operator1', '')
        value1 = cleaned_data.get('value1', '')
        condition = cleaned_data.get('condition', '')
        operator2 = cleaned_data.get('operator2', '')
        value2 = cleaned_data.get('value2', '')

        # Perform your validation logic here
        if (operator1 is not None and operator1 != '') and (value1 is None or value1 == ''):
            raise ValidationError("Value1 cannot be empty.")
        if (condition is not None and condition != '') and (operator2 is None or operator2 == ''):
            raise ValidationError(
                "Operator-2 cannot be blank.")
        elif (operator2 is not None and operator2 != '') and (value2 is None or value2 == ''):
            raise ValidationError("Value2 cannot be empty.")

        # Return cleaned data
        return cleaned_data
