from django import forms
from django.apps import apps
from django.conf import settings

from refenrencetype.models import RefValues


class CustomDashboardStatsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_reftype_id = getattr(settings, 'APPLICATION_APPNAMESFORDASHBOARD_REF_NO', '-1')

        app_names = RefValues.objects.filter(reftype_id=int(required_reftype_id)).values_list('value', 'display_value')

        self.fields['model_app_name'] = forms.ChoiceField(choices=[('', 'Select an option')] + list(app_names),
                                                          widget=forms.Select(attrs={
                                                              'onchange': 'populateModelNameByAppName()'
                                                          }))
        model_choices = [('', 'Select an option')]
        field_choices = [('', 'Select an option')]
        for app_value, _ in app_names:
            try:
                app_config = apps.get_app_config(app_value)
                models = app_config.get_models()
                for model in models:
                    model_choices.append((model.__name__, model._meta.verbose_name))
                    for field in model._meta.get_fields():
                        try:
                            field_choices.append((field.name, field.verbose_name))
                        except AttributeError:
                            field_choices.append((field.name, field.name))

            except LookupError:
                continue
        self.fields['model_name'] = forms.ChoiceField(choices=model_choices,
                                                      widget=forms.Select(attrs={
                                                          'onchange': 'populateDateOperationFieldNameByAppName()'
                                                      }))
        field_choices.append(('all', 'All'))
        self.fields['date_field_name'] = forms.ChoiceField(choices=field_choices)
        self.fields['operation_field_name'] = forms.ChoiceField(choices=field_choices)


class CustomChartSettingsForm(forms.Form):
    def __init__(self, stats, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for ch_filter in stats.criteriatostatsm2m_set.filter(use_as="chart_filter").order_by(
                "order"
        ):
            dy_map = ch_filter.get_dynamic_choices(user=user)
            if dy_map:
                self.fields[f"select_box_dynamic_{ch_filter.id}"] = forms.ChoiceField(
                    choices=[("", "-------")] + list(dy_map.values()),
                    label=ch_filter.criteria.criteria_name,
                    initial=ch_filter.default_option,
                )
                self.fields[f"select_box_dynamic_{ch_filter.id}"].widget.attrs[
                    "class"
                ] = "chart-input"

        self.fields["graph_key"] = forms.CharField(
            initial=stats.graph_key,
            widget=forms.HiddenInput(attrs={"class": "hidden_graph_key"}),
        )

        multiple_series = stats.criteriatostatsm2m_set.filter(use_as="multiple_series")
        if multiple_series.exists():
            choices = (
                multiple_series.select_related("stats__default_multiseries_criteria", "criteria")
                .order_by("order")
                .values_list("id", "criteria__criteria_name")
            )
            self.fields["select_box_multiple_series"] = forms.ChoiceField(
                label="Divide",
                choices=[("", "-------")] + list(choices),
                initial=(
                    stats.default_multiseries_criteria.id
                    if stats.default_multiseries_criteria
                    else None
                ),
            )
            self.fields["select_box_multiple_series"].widget.attrs[
                "class"
            ] = "chart-input select_box_multiple_series"
