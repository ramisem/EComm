from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _

import userauthentication
from core import models as core_models
from masterdata import models as masterdata_models


# Create your models here.
class Event_Rule(models.Model):
    FREQUENCY_UNIT_CHOICES = [
        ('sec', 'SECOND'),
        ('d', 'DAY'),
        ('m', 'MONTH'),
        ('y', 'YEAR'), ]
    event_rule_id = models.AutoField(primary_key=True, verbose_name="Event_RuleID")
    name = models.CharField(unique=True, max_length=80, null=True, verbose_name="Rule Name")
    iot_type_id = models.ForeignKey(core_models.IOT_Type, null=True, on_delete=models.CASCADE, verbose_name="IOT Type")
    event_type_id = models.ForeignKey(masterdata_models.Event_Type, null=True, on_delete=models.CASCADE,
                                      verbose_name="Event Type")
    is_active = models.BooleanField(
        _("Active"),
        default=True,
    )
    created_by = models.ForeignKey(userauthentication.models.User, null=True, blank=True, on_delete=models.CASCADE,
                                   verbose_name="Created By")
    rule_frequency = models.IntegerField(null=True, verbose_name="Frequency")
    rule_frequency_unit = models.CharField(null=True, max_length=40, choices=FREQUENCY_UNIT_CHOICES,
                                           verbose_name="Frequency Unit")
    event_iot_map_id = models.ForeignKey(masterdata_models.Event_Type_IOT_Type_Map, null=True, blank=True,
                                         on_delete=models.CASCADE, verbose_name="Event_Type_IOT_Type_Map_Id")

    class Meta:
        verbose_name = "Event Rule"
        verbose_name_plural = 'Event Rules'


class Event_Rule_Params(models.Model):
    OPERATOR_CHOICES = [
        ('=', '='),
        ('<', '<'),
        ('<=', '<='),
        ('>', '>'),
        ('>=', '>='), ]

    CONDITION_CHOICES = [
        ('and', 'AND'),
        ('or', 'OR'), ]

    event_rule_param_ispec_condition_id = models.AutoField(primary_key='true', verbose_name="Event Rule Parameter Id")
    event_rule_id = models.ForeignKey(Event_Rule, on_delete=models.SET_NULL, null=True, verbose_name="Event Rule Id")
    param_id = models.ForeignKey(masterdata_models.Param, on_delete=models.SET_NULL, null=True,
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

    class Meta:
        verbose_name = "Event Rule Parameter"
        verbose_name_plural = 'Event Rule Parameters'
        unique_together = ('event_rule_id', 'param_id')


auditlog.register(Event_Rule)
auditlog.register(Event_Rule_Params)
