from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.translation import gettext_lazy as _

import userauthentication


class IOT_Type(models.Model):
    iot_type_id = models.AutoField(primary_key=True, verbose_name="IOT_Type_Id")
    description = models.CharField(max_length=200, blank=True, null=True, verbose_name="Description")
    model_name = models.CharField(unique=True, max_length=40, verbose_name="IOT Type Name")
    model_id = models.CharField(unique=True, max_length=40, verbose_name="IOT Type")
    history = AuditlogHistoryField()

    class Meta:
        verbose_name = "IOT Type"
        verbose_name_plural = 'IOT Types'

    def __str__(self):
        return str(self.model_name)


class IOT_Device(models.Model):
    iot_device_id = models.AutoField(primary_key=True, verbose_name="IOT_Device_Id")
    name = models.CharField(max_length=80, verbose_name="Name")
    iot_type_id = models.ForeignKey(IOT_Type, on_delete=models.SET_NULL, null=True, verbose_name="Type")
    serialnumber = models.CharField(max_length=40, verbose_name="Serial #")
    externalid = models.CharField(max_length=80, verbose_name="External Id")
    description = models.CharField(max_length=200, blank=True, null=True, verbose_name="Description")
    manufacturer = models.CharField(max_length=200, blank=True, null=True, verbose_name="Manufacturer")
    uuid = ShortUUIDField(unique=True, length=40, max_length=40, verbose_name="UUId")
    created_dt = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created DateTime'), null=True, blank=True,
        help_text=_('In UTC'))
    created_by = models.ForeignKey(userauthentication.models.User, null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name="Created By")
    history = AuditlogHistoryField()

    class Meta:
        verbose_name = "Registered IoT Device"
        verbose_name_plural = 'Registered IoT Devices'

    def __str__(self):
        return self.uuid


auditlog.register(IOT_Type)
auditlog.register(IOT_Device)
