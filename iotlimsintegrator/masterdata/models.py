from auditlog.registry import auditlog
from django.db import models

from core import models as core_models


# Create your models here.
class Event_Type(models.Model):
    event_type_id = models.AutoField(primary_key=True, verbose_name="Event Type ID")
    event_name = models.CharField(max_length=80, verbose_name="Event Type")
    description = models.CharField(max_length=200, blank=True, null=True, verbose_name="Description")

    class Meta:
        verbose_name = "Event Type"
        verbose_name_plural = 'Event Types'

    def __str__(self):
        return str(self.event_name)


class Event_Type_IOT_Type_Map(models.Model):
    event_iot_map_id = models.AutoField(primary_key=True, verbose_name="Event IOT Type Id")
    event_type_id = models.ForeignKey(Event_Type, null=True, on_delete=models.CASCADE, verbose_name="Event Type Id",
                                      related_name="FK_Event_Type_Id")
    iot_type_id = models.ForeignKey(core_models.IOT_Type, null=True, on_delete=models.CASCADE, verbose_name="IOT Type",
                                    related_name="FK_IOT_Type")

    class Meta:
        verbose_name = "Event/IOT Type"
        verbose_name_plural = 'Event/IOT Types'
        unique_together = ('event_type_id', 'iot_type_id')

    def __str__(self):
        return str(self.event_iot_map_id)

    def __str__(self):
        return str(self.iot_type_id)


class Unit(models.Model):
    unit_id = models.AutoField(primary_key=True, verbose_name="Unit ID")
    unit_name = models.CharField(max_length=80, verbose_name="Unit", unique=True)

    class Meta:
        verbose_name = "Unit"
        verbose_name_plural = "Units"

    def __str__(self):
        return self.unit_name


class Param(models.Model):
    param_id = models.AutoField(primary_key=True, verbose_name="Param ID")
    param_name = models.CharField(max_length=80, verbose_name="Param Name", unique=True)
    vendor_param_id = models.CharField(blank=True, null=True, max_length=80, verbose_name="External Param Id", default='')
    description = models.CharField(max_length=200, verbose_name="Description", blank=True, null=True)
    unit = models.ForeignKey(Unit, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Param Unit",
                             related_name="FK_Param_Unit")

    class Meta:
        verbose_name = "Param"
        verbose_name_plural = "Params"
        unique_together = ('vendor_param_id', 'param_name')

    def __str__(self):
        return self.param_name


class EventRuleParams(models.Model):
    event_rule_param_id = models.AutoField(primary_key=True, verbose_name="Event Rule Param Id")
    event_type_iot_map_id = models.ForeignKey(Event_Type_IOT_Type_Map, null=True, on_delete=models.CASCADE,
                                              verbose_name="Event Type IOT Type Map Id",
                                              related_name="FK_Event_Type_IOT_Type_Map_Id")
    paramid = models.ForeignKey(Param, null=True, on_delete=models.CASCADE, verbose_name="Param Id",
                                related_name="FK_Param_Id")

    class Meta:
        verbose_name = "Event Rule Param"
        verbose_name_plural = "Event Rule Params"
        unique_together = ('event_type_iot_map_id', 'paramid')

    def __str__(self):
        return str(self.event_rule_param_id)


auditlog.register(Event_Type)
auditlog.register(Event_Type_IOT_Type_Map)
auditlog.register(Unit)
auditlog.register(Param)
auditlog.register(EventRuleParams)
