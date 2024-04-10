from django import forms

from .models import Event_Rule, Event_Rule_Params


class EventRuleForm(forms.ModelForm):
    class Meta:
        model = Event_Rule
        fields = ['name', 'event_type_id', 'iot_type_id', 'created_by', 'rule_frequency', 'rule_frequency_unit',
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
        if self.instance.param_id:
            self.fields['param_id'].disabled = True

    class Meta:
        model = Event_Rule_Params
        fields = ['param_id', 'operator1', 'value1', 'value1_unit', 'condition', 'operator2', 'value2', 'value2_unit',
                  'value_text', 'duration', 'unit_name']
        widgets = {
            'value1': forms.TextInput(attrs={'onchange': 'populateParamUnit(this.id)'}),
            'value2': forms.TextInput(attrs={'onchange': 'populateParamUnit(this.id)'}),
        }
