from django.db import models
from shortuuid.django_fields import ShortUUIDField


class IOT_Type(models.Model):
    iot_type_id = models.AutoField(primary_key=True, verbose_name="IOT_Type_Id")
    description = models.CharField(max_length=200, verbose_name="Description")

    class Meta:
        verbose_name = "IOT Type"
        verbose_name_plural = 'IOT Types'

    def __str__(self):
        return str(self.description)


class IOT_Device(models.Model):
    iot_device_id = models.AutoField(primary_key=True, verbose_name="IOT_Device_Id")
    name = models.CharField(max_length=80, verbose_name="Name")
    iot_type_id = models.ForeignKey(IOT_Type, on_delete=models.SET_NULL, null=True, verbose_name="Type")
    serialnumber = models.CharField(max_length=40, verbose_name="Serial #")
    externalid = models.CharField(max_length=80, verbose_name="External Id")
    description = models.CharField(max_length=200, verbose_name="Description")
    manufacturer = models.CharField(max_length=200, verbose_name="Manufacturer")
    uuid = ShortUUIDField(unique=True, length=40, max_length=40, verbose_name="UUId")

    class Meta:
        verbose_name = "IOT Device"
        verbose_name_plural = 'IOT Devices'

    def __str__(self):
        return self.uuid
