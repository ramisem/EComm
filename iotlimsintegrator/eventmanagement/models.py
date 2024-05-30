from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _

import apidetails
import userauthentication
from core import models as core_models
from masterdata import models as masterdata_models


# Create your models here.
class Event_Rule(models.Model):
    event_rule_id = models.AutoField(primary_key=True, verbose_name="Event_RuleID")
    name = models.CharField(unique=True, max_length=80, null=True, verbose_name="Rule Name")
    iot_type_id = models.ForeignKey(core_models.IOT_Type, null=True, on_delete=models.CASCADE, verbose_name="IOT Type")
    event_type_id = models.ForeignKey(masterdata_models.Event_Type, null=True, on_delete=models.CASCADE,
                                      verbose_name="Event Type")
    created_dt = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created DateTime'), null=True, blank=True,
        help_text=_('In UTC'))
    created_by = models.ForeignKey(userauthentication.models.User, null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name="Created By")
    inbound_api = models.ForeignKey(apidetails.models.APIDetail, on_delete=models.CASCADE,
                                    verbose_name="EM API", related_name='inbound_api_related',
                                    limit_choices_to={'type': 'inbound'})
    outbound_api = models.ForeignKey(apidetails.models.APIDetail, on_delete=models.CASCADE,
                                     verbose_name="LIMS API", related_name='outbound_api_related',
                                     limit_choices_to={'type': 'outbound'})
    event_iot_map_id = models.ForeignKey(masterdata_models.Event_Type_IOT_Type_Map, null=True, blank=True,
                                         on_delete=models.SET_NULL, verbose_name="Event_Type_IOT_Type_Map_Id")
    history = AuditlogHistoryField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Event Rule"
        verbose_name_plural = 'Event Rules'


class Event_Rule_Params(models.Model):
    OPERATOR_CHOICES = [
        ('==', '='),
        ('<', '<'),
        ('<=', '<='),
        ('>', '>'),
        ('>=', '>='), ]

    CONDITION_CHOICES = [
        ('and', 'AND'),
        ('or', 'OR'), ]

    event_rule_param_ispec_condition_id = models.AutoField(primary_key='true', verbose_name="Event Rule Parameter Id")
    event_rule_id = models.ForeignKey(Event_Rule, on_delete=models.CASCADE, verbose_name="Event Rule Id")
    param_id = models.ForeignKey(masterdata_models.Param, on_delete=models.CASCADE,
                                 verbose_name="Parameter ID")
    operator1 = models.CharField(null=True, blank=True, max_length=40, choices=OPERATOR_CHOICES,
                                 verbose_name="Operator-1")
    value1 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2, verbose_name="Value1", )
    condition = models.CharField(null=True, blank=True, max_length=40, choices=CONDITION_CHOICES,
                                 verbose_name="Condition")
    operator2 = models.CharField(null=True, blank=True, max_length=40, choices=OPERATOR_CHOICES,
                                 verbose_name="Operator-2")
    value2 = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2, verbose_name="Value2", )
    value_text = models.CharField(null=True, blank=True, max_length=80, verbose_name="Condition(In Text)")
    duration = models.IntegerField(null=True, blank=True, verbose_name="Duration")
    unit_name = models.ForeignKey(masterdata_models.Unit, on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name="Duration Unit")
    history = AuditlogHistoryField()

    def evaluate_condition1(self, input_value):
        expression = f"{input_value} {self.operator1} {self.value1}"
        return eval(expression)

    def evaluate_condition2(self, input_value):
        expression = f"{input_value} {self.operator2} {self.value2}"
        return eval(expression)

    def execute_event_rule_condition_evaluation(self, data):
        if not data:
            raise Exception('Data object cannot be obtained.')
        if not isinstance(data, dict):
            raise Exception('Data object should be a Dictionary object.')
        param_id = self.param_id.param_id
        if self.param_id.vendor_param_id:
            param_id = self.param_id.vendor_param_id
        param_value = data[param_id]
        if param_value is None:
            return None
        if (self.value1 is None or self.value1 == '') and (self.value_text is None or self.value_text == ''):
            raise Exception('Both Value1 and Condition cannot be blank.')
        if self.value_text is not None and self.value_text != '':
            if self.value_text == param_value:
                result_for_each_param = {
                    'param_id': param_id,
                    'condition_evaluation': True
                }
            else:
                result_for_each_param = {
                    'param_id': param_id,
                    'condition_evaluation': False
                }
            return result_for_each_param
        if self.condition is None or self.condition == '':
            result_for_each_param = {
                'param_id': param_id,
                'condition_evaluation': self.evaluate_condition1(param_value)
            }
            return result_for_each_param
        if self.value2 is None or self.value2 == '':
            raise Exception('value2 cannot be blank.')
        if 'or' == self.condition:
            result_for_each_param = {
                'param_id': param_id,
                'condition_evaluation': self.evaluate_condition1(
                    param_value) or self.evaluate_condition2(param_value)
            }
        else:
            result_for_each_param = {
                'param_id': param_id,
                'condition_evaluation': self.evaluate_condition1(
                    param_value) and self.evaluate_condition2(param_value)
            }
        return result_for_each_param

    class Meta:
        verbose_name = "Rule Parameter"
        verbose_name_plural = 'Rule Parameters'
        unique_together = ('event_rule_id', 'param_id')


auditlog.register(Event_Rule)
auditlog.register(Event_Rule_Params)
